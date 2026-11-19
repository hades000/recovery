---
title: "Security review: RWB-TE-001 Recovery module folder and boundary test"
run_id: "INC-002-epic-1-RWB-TE-001"
story: "RWB-TE-001"
stage: "review"
reviewer: "security reviewer (mandatory pre-merge security review)"
date: "2026-11-18"
diff: "git -C rwb-wt/RWB-TE-001 diff develop-recovery...feature/RWB-TE-001-module-boundary (225 files, +3632/-177)"
status: "PASS"
---

# Security review — RWB-TE-001

## Verdict

**PASS.** No Critical and no High security defect in the change.

| Severity | Count |
|---|---|
| Critical | 0 |
| High | 0 |
| Medium | 1 |
| Low | 0 |

The one Medium finding is an inherited weakness in the frontend lint allow-list that this branch
does not modify. It is an architecture-guard bypass, not an access-control defect, and it does not
block the structural merge; it is reported because the new AC6 test is presented as proof that the
guard cannot be bypassed, and it does not prove that (finding SEC-TE001-01).

## Findings

### SEC-TE001-01 — D-RCV-39 import allow-list is bypassed by `..` path segments inside an allowed prefix (Medium)

**Pre-existing:** the rule at `frontend/eslint.config.js:15` and `:19` is unchanged by this branch.
**Made visible by this diff:** `frontend/src/modules/recovery/__tests__/importBoundary.test.ts:13-22`
and `:51-57` assert the rule fires for eight rejected forms, but every one of them either starts at
the first segment with `../` or is an `@/` import outside the allow-list; none hides `..` behind an
allowed prefix, so the test certifies a control that still has a hole.

**Concrete failure case**

1. The alias is `@` → `<frontend>/src` (`frontend/vite.config.ts:11`, `frontend/tsconfig.json` paths
   `"@/*": ["src/*"]`).
2. In a real recovery file, `frontend/src/modules/recovery/caselist/X.tsx`, write:
   ```tsx
   import { WorkList } from "@/components/ui/../../modules/collection/worklist/WorkList";
   ```
   The specifier starts with an allowed prefix, so the negative lookahead at
   `frontend/eslint.config.js:19` does not match, and the path resolves to
   `src/modules/collection/worklist/WorkList` — outside the recovery folder.
3. Two more forms behave the same: `"@/modules/recovery/../../collection/worklist/WorkList"` (the
   `modules/recovery/` alternative is an allowed prefix) and `"./../collection/worklist/WorkList"`
   (the `group: ["../*", "../**"]` at `eslint.config.js:15` only matches specifiers whose first
   segment is literally `..`).
4. Verified against the real config, not by inspection:
   `new ESLint({cwd: "frontend"}).lintText(source, {filePath: "src/modules/recovery/caselist/BoundaryFixture.tsx"})`
   returned `messages: []` for all three specifiers above, while
   `@/modules/collection/worklist/WorkList` returned `no-restricted-imports`. `npm run lint` and the
   new AC6 test therefore stay green on a genuine D-RCV-39 violation; in the ACE front end, where the
   collection module exists, `tsc`/`vite build` also resolve the path instead of failing on it.

**Impact.** A recovery component can take a compile-time dependency on the collection module
internals (which hold customer data in ACE) with a green pipeline — the exact violation AC6 and
D-RCV-39 exist to prevent — and the story's AC6 evidence overstates what is enforced. There is no
direct data read or privilege escalation from the lint bypass itself, and the odd specifier is
visible in human review, so this is Medium rather than High. It requires a developer to write the
path deliberately.

**Smallest fix.** Add one pattern to `recoveryImportRule` in `frontend/eslint.config.js`:

```js
{ regex: "\\.\\.", message: "D-RCV-39: no '..' path segments in the recovery module." },
```

(verified as a RegExp against the three bypassing and the seven allowed specifiers: only the three
match), then add those three specifiers to `rejected` in `importBoundary.test.ts` so the test would
catch a regression. No other config or dependency change is needed.

## Checked and clean

### Secrets, credentials and personal data

- Scanned all 225 changed files for keys, tokens, connection strings, passwords, Bearer values,
  e-mail addresses, national/account-number shapes and high-entropy strings. No real secret.
- The only key-shaped value is a synthetic all-`A` Azurite account key for `devstoreaccount1` at
  `127.0.0.1` in `backend/src/test/java/th/co/scb/ace/demo/recovery/dochub/storage/BlobDocumentStoreTest.java:152-155`.
  It is a local emulator placeholder, is not a working credential, and never leaves test scope.
- Codec keys are generated per run with `SecureRandom` (not committed):
  `TemporalConfigTest.java:92-96`, `PdpaPayloadCodecTest.java:18-22`.
- JWT and PII fixtures are explicitly synthetic: `"Bearer token"` with a mocked decoder
  (`SecurityConfigTest.java:99-110`), `synthetic-user` (`:156`), `"Synthetic Person"`
  (`PdpaPayloadCodecTest.java:34`), zero-padded UUIDs (`BlobDocumentStoreTest.java:39`). No real
  name, ID, account number, address or e-mail anywhere in the diff.
- `backend/src/main/resources/application*.yaml` is not changed; every secret-valued key there is an
  `${ENV:default}` placeholder with an empty default (`RWB_MIGRATOR_PASSWORD`, `RWB_TEMPORAL_CODEC_KEY`,
  `RWB_BLOB_CONNECTION_STRING`).

### Module-map loader — path, YAML and input safety

`backend/src/test/java/th/co/scb/ace/demo/recovery/architecture/boundary/ModuleMapLoader.java`

- **Path traversal: not reachable.** The only callers pass fixed test paths —
  `RecoveryBoundaryTest.java:40-41`, `BoundaryRulesTest.java:33-35`, `ModuleMapLoaderTest.java`.
  The loader never derives a path from YAML; `rootPackage` (validated by `PACKAGE`, line 30, which
  forbids `.`/`..` segments and `/`) is only used as a package string.
- **YAML bomb / alias expansion: bounded.** `SafeConstructor` (line 177) plus SnakeYAML 2.6
  `LoaderOptions` defaults: `maxAliasesForCollections = 50`, `nestingDepthLimit = 50`,
  `codePointLimit = 3 MiB` (confirmed with `javap` on `snakeyaml-2.6.jar`; SnakeYAML comes in
  transitively, no dependency was added). `allowDuplicateKeys(false)` is set explicitly at line 176.
- **Arbitrary object construction: blocked.** `SafeConstructor` refuses `!!` class tags, so YAML
  cannot instantiate a class or execute code; `UnTrustedTagInspector` is the 2.6 default.
- **Entity expansion: not applicable.** SnakeYAML parses YAML, not XML.
- **Duplicate keys / unknown keys / wrong shapes: rejected with file and field path**
  (`ModuleMapLoaderTest.java:136-230`), including non-string keys (line 273-274).
- **Unbounded input: residual robustness nit, not exploitable.** `Files.readString` (line 169) reads
  the whole file before the 3 MiB parse cap; a multi-GB map would OOM the test JVM. But the map is a
  repository file behind code-owner review (D-RCV-21), so writing it requires the same access as
  changing the build or the tests. No external input path exists.
- **Symlinks:** a symlinked map would be followed, but placing a symlink in the tree is again a
  commit-level action, not a privilege boundary. Not a finding.

### Dependency and build-script injection

- No new dependency. `backend/build.gradle.kts` changes only the JaCoCo counters (LINE, INSTRUCTION,
  BRANCH, METHOD at 0.80) and the class/source directories to add the test-scope `architecture/boundary`
  tooling (lines 130-170). No `exec`, no network, no environment or property interpolation into a
  command, no plugin, no repository. `frontend/package.json` and lock file are untouched.
- The new frontend test uses the already-declared `eslint` devDependency and the ESLint Node API; no
  new package and no shell execution.
- Nothing in the diff consumes untrusted input at build time (the map is repo content, validated as
  above).

### Authentication and authorization after the package moves

- No endpoint was added, removed or re-pathed. The only two controllers still expose the same two
  paths and both keep their method checks:
  `casewf/admin/TemporalAdminController.java:68` (`hasAnyAuthority('RW-PLATADM','RW-AUDIT')`) and
  `:93` (`hasAuthority('RW-PLATADM')`); `integration/internal/PlatformInfoController.java:33`
  (`isAuthenticated()`). `SecurityConfig` still has `anyRequest().denyAll()` and
  `/api/recovery/**` → `HOLDS_WORKBENCH_ROLE` (`access/internal/SecurityConfig.java:68-73`).
- `SecurityConfig`, `ApiExceptionHandler` and `ProblemFactory` are still package-private and still
  under the `th.co.scb.ace.demo` component scan (application class
  `th/co/scb/ace/demo/AceRecoveryApplication.java`), so they are still registered. `@EnableMethodSecurity`
  is still on the same configuration class; the new test proves method security still applies after
  the move (`SecurityConfigTest.java:82-88` 403 MSG-P4-002, `:97-112` roles-claim mapping).
- Behaviour is unchanged: the `SecurityConfig` body differs only in the property source
  (`RecoveryProperties.security()` → `RecoverySecurityProperties`), with the same keys
  (`rwb.security.issuer`, `jwk-set-uri`, `audience`, `roles-claim`, `cors-origins`), the same
  issuer/audience validation, and the same CORS origins and headers
  (`access/internal/SecurityConfig.java:85-119`, `access/internal/RecoverySecurityProperties.java`).
  `application*.yaml` keys and defaults are unchanged.
- `ApiExceptionHandler` still applies to the whole recovery tree (`basePackages =
  "th.co.scb.ace.demo.recovery"`), so the moved controllers keep their problem bodies.
- Visibility changes are narrow and safe: `PdpaPayloadCodec` public → package-private (reduces
  reach, only `TemporalConfig` and its own tests use it); `TemporalProperties` package-private →
  public (read by `casewf.admin`, same Spring module, package is not published — verified no
  `@NamedInterface` under any `internal` package). The key accessor is not exposed through an
  endpoint: actuator exposure is limited to health/info/prometheus/metrics
  (`application.yaml:39-43`), and `configprops`/`env` are not exposed.
- No `@PreAuthorize`, `@Secured` or `@RolesAllowed` was removed anywhere in the diff, and no test was
  disabled or loosened (`@Disabled`, `assumeTrue`, `skip` searches found nothing).

### Logs and fixtures

- No new or changed log line carries a person, an identifier or a business value. The changed log
  statements (unchanged text, moved classes) log a message code, a flag value, a task-queue name or a
  cache size only (`ApiExceptionHandler.java:35`, `TemporalConfig.java:78`,
  `DroolsRuleEngine.java:64`). `ProblemFactory` puts a trace ID, not payload data, in the error body.
- `ApiExceptionHandler` never returns exception text or a stack trace to the client (the catch-all
  returns a bare 500), and the test asserts that (`ApiExceptionHandlerTest.java:60-68`).
- Boundary fixtures contain class and package names only (`th.co.scb.ace.boundaryfixture.*`), no
  data. Loader failure text prints a file, a field path and the rule text, never values from a real
  record.

## Advisory (not a security finding, not counted)

`RecoveryBoundaryTest.java:46-47` hard-codes `PUBLISHED_PACKAGES` instead of deriving it from the
module map, which reads against BR6 ("names, packages and published packages come from the map, not
the test"). It fails closed (an unexpected published package makes the test fail), so it has no
security effect; recorded for the code/architecture gate.

## Method and evidence

- Reviewed the full three-dot diff and the complete final content of every changed main class, the
  new loader/rules/tests, the map and fixture YAML, `build.gradle.kts`, `frontend/eslint.config.js`,
  `frontend/vite.config.ts` and `frontend/tsconfig.json`.
- The ESLint bypass was reproduced by running the repository's real `eslint.config.js` through its
  installed ESLint 9.39.5 with `lintText` on the same fixture path the new test uses; it was not
  inferred from reading the regex.
- SnakeYAML limits were read from the resolved `snakeyaml-2.6.jar` with `javap`, not assumed.
- No code, test, plan or shared file was modified by this review. No Jira, Confluence or GitLab
  system was consulted; none is connected (RUN-BRIEF rule 5).

## Fix round 1 verification (SEC-TE001-01)

**Range:** `bedecbd` (red fixtures) → `3cb6c9d` (green fix). Re-read
`frontend/eslint.config.js:19-24` (new `regex: "^(?!\\.\\./).*\\.\\."`) and
`frontend/src/modules/recovery/__tests__/importBoundary.test.ts:22-24` (the three new rejected
fixtures).

**Verdict: CLOSED.** The Medium finding is resolved; no residual security issue. Open security
findings after round 1: Critical 0, High 0, Medium 0, Low 0. Overall verdict remains **PASS**.

**Reproduction against the real config** (ESLint 9.39.5, `lintText` on
`src/modules/recovery/caselist/BoundaryFixture.tsx`, 19 specifiers):

| Specifier | `no-restricted-imports` |
|---|---|
| `@/components/ui/../../modules/collection/worklist/WorkList` | 1 |
| `@/modules/recovery/../../collection/worklist/WorkList` | 1 |
| `./../collection/worklist/WorkList` | 1 |
| `../x`, `../../collection/worklist/WorkList` | 1 each, not 2 |
| `./sibling`, `./casewf/child`, `@/modules/recovery/casewf/x` | 0 |
| `@/components/ui/button`, `@/lib/utils`, `@/utils/date`, `@/contexts/ApiClientContext`, `@/api/schema` | 0 |
| original rejected set (`@/modules/collection/...`, `@/hooks/cfsc/x`, `@/api/tdr/config`, `@/pages/x`, `@/utils/cfscCaseList`, `@/modules/other/x`) | 1 each |

The two patterns are disjoint by construction: the `../*`/`../**` group owns specifiers whose
first segment is `..` (hence the regex's `(?!\.\./)`), and the regex owns every other specifier
containing `..`. That gives exactly one message per `..` import, which the `../x` row confirms.

**Committed test and false positives:** `node node_modules/vitest/vitest.mjs run
src/modules/recovery/__tests__/importBoundary.test.ts` → 1 file, 18 tests passed. A full
`node node_modules/eslint/bin/eslint.js .` in `frontend/` exits 0, so the tightened rule rejects
no legitimate import in the existing tree.

**Residual (cosmetic, no security effect):** the regex matches any `..` substring rather than only
a `..` path segment, so a pathological file name such as `./a..b.ts` would also be reported. No such
import exists and the whole tree lints clean; if the team wants exactness, `(^|/)\.\.(/|$)` is the
narrower form. Also noted: the other changes in `3cb6c9d` (exact-package match for the external BND-1/
BND-2 entry, Thai text, dead code) tighten or do not touch the boundary; none weakens a security
control.

