# Assumptions: RWB-TE-002 implement stage

No question was asked (L-RCV-03). Spec ASM-TE002-01..-18 and plan PA-01..PA-14 are carried.

| ID | Assumption | Basis | Effect if wrong |
|---|---|---|---|
| IA-01 | The untracked codeowners folder left by an earlier run is acceptable as the TASK-01 starting point because its stubs match `data-model.md` §1.1 and every assertion matches §1.3/§1.4 and `tests/scenarios.md`; it was re-run red by this stage before any logic. One fixture fix: UT-19 patterns now carry the leading `/` the grammar requires. | Orchestrator instruction (keep only what the plan wants and what is shown red then green); `red-task01-03.txt`. | Rewrite the affected test; no production code depends on it. |
| IA-02 | V5 is evaluated per section block (see `deviations.md` DEV-05). | UT-23 fixture B expects one duplicate error. | Only V5's key changes; the live file has no repeated header. |
| IA-03 | A register `owners` value that is not a list is reported as `owners is missing`; a `reservedPatterns` value that is not a list is ignored. | `data-model.md` §1.3 has no separate text for these cases. | One more V11 text and a test case. |
| IA-04 | A YAML parse error is reported with the first line of the SnakeYAML message only. | `register: invalid YAML: {problem}`; keeps the finding one line. | Message detail only. |
| IA-05 | The full `./scripts/dev.ps1 test` is run once at the final tip (orchestrator time box); targeted Gradle runs are the per-task evidence. | Orchestrator instruction. | None on results. |
