What this change does: It moves 26 classes and 4 tests out of the four old packages into 19 design modules (`casewf`, `integration`, `dochub`, `access`, and the rest), and splits the one shared settings record into four per-module records. It also adds 61 `package-info` markers, a test-only module map with a loader, five map-driven ArchUnit rules, a JaCoCo gate at 80% on four counters, and a Vitest test that runs the real ESLint import rule. I judged it at the load it will see: every developer build and CI run (a few hundred recovery classes plus about 150 fixture classes), and one local stack; no user traffic path changes.

**Must fix**

1. **The Thai API messages are now garbage** (`backend/src/main/java/th/co/scb/ace/demo/recovery/access/api/ApiError.java:19,24,29,34`)
   - **What this is:** `ApiError` holds the English and Thai text of the four problems the platform returns itself (401, 403, 404, 503). `ProblemFactory` puts the Thai text in every `messageTh` field, and the front end shows `messageTh` when the language is Thai, which is the default.
   - **Problem:** The move re-encoded the file. All four Thai literals are now Latin-1 mojibake (`"à¸„à¸¸à¸“à¸¢..."`). The base file has the correct Thai, and the only intended change is the package line, so this is an accident, not a decision. Every Thai user gets a broken message on the login, permission, not-found and Temporal-down paths; the tests miss it because they look only for the Latin placeholder. The same re-encoding also turned `§` into `Â§` in `ApiExceptionHandler.java:20`, `TemporalAdminController.java:66` and `PlatformSmokeWorkflowTest.java:23`.
   - **Fix:** Copy the four `messageTh` strings from `develop-recovery`'s `backend/src/main/java/th/co/scb/ace/demo/recovery/platform/api/ApiError.java` (and the three `§` comments) into the new files. The new `ApiError` should differ from the old one only in its `package` line.
   - **If we skip it:** Thai users see mojibake for every platform error, and the API returns text that no longer matches the Error and Message Standard.

2. **BND-1 and BND-2 let sub-packages of a published external package through** (`backend/src/test/java/th/co/scb/ace/demo/recovery/architecture/boundary/BoundaryRules.java:224-226`)
   - **What this is:** BND-1 and BND-2 stop recovery code calling the inside of the `collection` and `common` modules; only their published packages may be used. The map lists `common.api` and `collection.api`.
   - **Problem:** The check uses `isUnder(targetPackage, external.rootPackage + "." + entry)`, which also accepts every sub-package. A recovery class that imports `th.co.scb.ace.demo.common.api.internal.SecretHelper` passes BND-2, although `common.api.internal` is not the published `common.api` package. The module-map rule and SPEC-001's `propagate = false` rule both treat sub-packages as unpublished, so this rule is looser than the rest of the story. The fixtures use `common.internal` (not under `api`), so no test catches it.
   - **Fix:** Compare the package exactly: `anyMatch(entry -> target.getPackageName().equals(external.rootPackage() + "." + entry))`. Add one fixture class in `common/api/internal` used by a `casewf` class, and assert the extra BND-2 line.
   - **If we skip it:** A future change that imports a class from a sub-package of an ACE published package builds green, although it is exactly the cross-module call this story is meant to stop.

**Should fix**

3. **The Thai tests cannot fail when the Thai text is wrong** (`backend/src/test/java/th/co/scb/ace/demo/recovery/access/api/ApiErrorTest.java:31`, `backend/src/test/java/th/co/scb/ace/demo/recovery/access/internal/ApiExceptionHandlerTest.java:40`)
   - **What this is:** Two new tests claim to check placeholder fill in English and Thai.
   - **Problem:** Both assert only `contains("approve")`, which is the Latin placeholder, so they pass on the mojibake Thai strings. Nothing in the suite checks the Thai text.
   - **Fix:** Assert the exact expected Thai string for `NOT_PERMITTED` in `ApiErrorTest`, and the exact Thai for that problem in `ApiExceptionHandlerTest`. The mojibake value fails both assertions.
   - **If we skip it:** The encoding bug in finding 1, or any later edit to the Thai text, is invisible to `./scripts/dev.ps1 test`.

**Nice to have**

4. **Five same-package imports left by the move** (`backend/src/main/java/th/co/scb/ace/demo/recovery/casewf/rules/DroolsRuleEngine.java:30-34`)
   - **What this is:** After the move, `DroolsRuleEngine` is in `casewf.rules` but still imports `CompiledRulePackage`, `RuleEngine`, `RuleInput`, `RuleOutcome` and `RuleResult` from that same package.
   - **Problem:** The five lines do nothing and make a reader check whether those classes live somewhere else.
   - **Fix:** Delete the five imports.
   - **If we skip it:** Five dead lines stay in a class every rules change touches.

5. **`moduleFor` carries an unused map parameter** (`backend/src/test/java/th/co/scb/ace/demo/recovery/architecture/boundary/BoundaryRules.java:87-89,231`)
   - **What this is:** The BND-1/BND-2 text helper `moduleFor(map, external)` returns `external.name()` and never reads `map`.
   - **Problem:** Dead input, and it hints that the map affects the text when it does not.
   - **Fix:** Use `external.name()` at line 231 and delete the helper.
   - **If we skip it:** A reader looks for a map lookup that is not there.

First-round verdict: fix 1 and 2 first.

Lean: -8 lines possible.

Not checked at first review: I did not run the Gradle build, the JaCoCo gate, `ModulithTest`/ArchUnit, Vitest or Playwright, or the local stack; findings 1 and 2 come from reading the code, the base file and the fixtures. HV-01 (GitLab merge blocking) remains a human check.

## Fix round 1 verification

Checked `bedecbd` (red tests), `3cb6c9d` (green) and the current tree. The red tests would fail on the old code (correct Thai against the mojibake enum, `SecretHelper` against the old `isUnder`, the three bypass cases against the old ESLint config). In the green tree the targeted backend classes and the frontend import test (18 cases) pass; `eslint src/modules/recovery` exits 0.

| Finding | Verdict | Evidence |
|---|---|---|
| 1. Thai `messageTh` | Closed | `ApiError.java` is case-sensitively identical to `8675a5c` except line 1; all 70 remaining lines compare equal, including all four Thai strings. No mojibake is left in `backend` or `frontend`, and the three `§` comments are restored. |
| 2. External sub-package | Closed | `BoundaryRules.java:222` compares the target package exactly. `SecretHelper` in `common.api.internal` is reported, `CustomerLookup` in `common.api` is not, and `BoundaryRulesTest` passes 17/17. |
| 3. Thai tests | Closed | `ApiErrorTest` and `ApiExceptionHandlerTest` assert the exact 57-code-point Thai string; it equals the enum value with `{action}` filled. Only `NOT_PERMITTED` is pinned, so a single-constant edit of the other three would still pass (minor). |
| 4. Same-package imports | Closed | The five imports are gone; `DroolsRuleEngine` now imports only `RecoveryFlags`. The targeted build and tests pass; no behaviour change. |
| 5. `moduleFor` parameter | Closed | The helper is deleted and the call uses `external.name()`, producing the same text. The targeted tests pass. |

New findings:

6. **Nice to have: the new `..` lint pattern double-reports some forms** (`frontend/eslint.config.js:18-24`). Verified with the real ESLint API: `@/api/schema/../x` gets two `no-restricted-imports` messages, because both the new pattern and the `@/` pattern match. The three added bypass cases each get one, and the import is still rejected, so this is cosmetic. Fix: exclude sources the `@/` pattern already reports from the new pattern, or let the test helper accept at least one; add that form to the rejected set.
7. **Note: the fix changes `frontend/eslint.config.js`, which the plan and SPEC-013/014/017 list as unchanged.** It is a tightening, not a weakening, and the three new rejected cases cover it. Record it in the plan/spec/PR (or split it out), so the next story does not treat the file as untouched.

Verdict: **Ship.** All five findings are closed. Finding 6 is a cosmetic duplicate, finding 7 is a scope note, and no test was removed, skipped or weakened and no coverage exclusion was added.
