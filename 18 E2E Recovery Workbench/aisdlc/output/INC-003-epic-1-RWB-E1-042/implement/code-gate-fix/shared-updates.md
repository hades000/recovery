# Shared updates from the code-gate fix round (commit `9056ed2`)

Run `INC-003-epic-1-RWB-E1-042`. Per RUN-BRIEF rule 3 this stage edits no shared file; the
orchestrator applies these rows. They add to `implement/shared-updates.md`, they do not replace it.

## 1. `aisdlc/requirement/Traceability_Matrix.md`

| Story | SPEC | Code | Test |
|---|---|---|---|
| RWB-E1-042 | SPEC-013 (identical repeat of a VALIDATED **or APPROVED** load), §12.5 checks 11 and 12 | `ParameterLoadHandlerImpl#load`, `ParameterLoadValidator#validateApprovalWindow` (code-gate CODE-001) | TC-E1-042-16: `ParameterConfigIT#anApprovedLoadRepeatsInsteadOfBeingRefused`, `ParameterLoadHandlerTest#anApprovedLoadRepeatsBeforeTheApprovedFromCheck`, `#aDifferentLoadStillMeetsTheApprovedFromCheck`; check 12: `ParameterLoadValidatorTest#anApprovedVersionOnOrAfterTheDateIsARefusal409`, `ParameterConfigIT#conflictingContentIsRefused` |

## 2. For later stories

| Story | Row |
|---|---|
| RWB-E1-043 | Re-submitting the same file and `validFrom` after the load was **approved** now returns the existing load with `repeat = true` and status `APPROVED` (no 409). A different file for the same (key, environment) dated on or before an approved row is still 409 `MSG-P3-027`. |

## 3. `aisdlc/docs/open-items.md`

None.

## 4. Code-gate round 2 (commits `216a696`, `25c8f94`; proposals only, nothing here is applied)

### `aisdlc/requirement/Traceability_Matrix.md`

| Story | SPEC | Code | Test |
|---|---|---|---|
| RWB-E1-042 | SPEC-014 (concurrent approval, 409 `MSG-GEN-004`) | `ParameterLoadHandlerImpl#approve`, `ParameterValueRepository#lockByLoadId` | TC-E1-042-20: `ParameterConfigIT#concurrentApprovalsGiveOneApprovedAndOne409` (system, two threads, latch) |
| RWB-E1-042 | SPEC-021 (flag-off contract) | `ParameterLoadHandlerImpl` (`@ConditionalOnProperty`) | TC-E1-042-22: `ParameterConfigIT#flagOnLoadsThroughTheAdapter`, `ParameterConfigIT$FlagOff#flagOffStillStartsAndRefusesParameterLoads` (test-only `ParameterLoadBranch` adapter) |
| RWB-E1-042 | SPEC-012, SPEC-023 | `ParameterLoadValidator#validate` | TC-E1-042-23: `ParameterConfigIT#unknownKeyEmptyFileAndPastValidFrom` (system) |

### For later stories

| Story | Row |
|---|---|
| RWB-E1-043 | The real `ParameterLoadBranch` is still yours. This story's flag-off and flag-on cases use a test-only stand-in with the same shape (`ObjectProvider<ParameterLoadHandler>`, 404 `MSG-P4-003` when absent). The HTTP-level refusal stays with E43S TC-PB-01 and TC-FL-01. |

### Deviation numbering

`implement/deviations.md` holds DEV-01..DEV-12, DEV-19 and DEV-20 (DEV-20 maps six planned test names in `plan/tests/scenarios.md` to the tests that ran; the traceability rows for T-E1-042-04, -10(b), -17, -28, -32 and -44 should cite the actual names in its table). `implement/review-fix/deviations-review-fix.md`
holds DEV-13..DEV-18. Any shared row that cites the check-12 reorder must cite **DEV-19**, not DEV-13.
