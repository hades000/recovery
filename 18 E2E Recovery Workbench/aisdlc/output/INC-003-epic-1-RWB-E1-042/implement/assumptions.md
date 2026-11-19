# Implementation assumptions

Run `INC-003-epic-1-RWB-E1-042`. No question was put to a user (L-RCV-03, AGENTS §10.6). The spec's 25
open items and the plan's `PA-E1-042-01..-17` were carried unchanged; the rows below are what the code
had to decide while implementing.

| ID | Assumption | Basis | Where it shows |
|---|---|---|---|
| IA-01 | The business date is "today in Asia/Bangkok" until a platform provider arrives | Spec SPEC-023 and `data-model.md` §3; the zone is the application's configured `Asia/Bangkok` | `InterimBusinessDateProvider` |
| IA-02 | `ParameterService.get` resolves the **running** environment (`rwb.environment`), and the catalog endpoint resolves the **requested** one | Spec §7.5 (query `environment`, else `rwb.environment`) and §12.2 | `ParameterServiceImpl.resolve` vs `inEnvironment` |
| IA-03 | A parameter's `value_source` and `scope` tokens are compared as the catalog writes them (`"ENV"`, `"TABLE"`, `"SECRET"`, `"GLOBAL"`, `"PRODUCT"`), because the catalog parser refuses any other value | `data-model.md` §3, §7.1 | `ParameterServiceImpl`, `ParameterLoadValidator`, `ParameterStartupCheck` |
| IA-04 | A load of a key with no earlier approved version is refused at **rollback**, not at approval | Spec §8 transition table (`APPROVED` → `ROLLED_BACK` only when every row has an earlier version) | `ParameterLoadHandlerImpl.rollback` |
| IA-05 | The last seeded value row's `valid_to` stays NULL; only rows that a later approval supersedes get an end date | Spec §12.7 | `ParameterValidity` |
| IA-06 | An identical repeat is detected by `(validFrom, content_hash)` before the write and again after a unique violation, so a re-run is harmless and never a 500 | Spec SPEC-013, §12.7 | `ParameterLoadHandlerImpl.load` |
| IA-07 | The 40 seeded value rows use `version_no 1`, `status APPROVED`, `valid_from 2026-11-02` and the synthetic seed identity `00000000-0000-0000-0000-0000000e1042` | `data-model.md` §4.4 (A-04, A-05) | The migration |
| IA-08 | A message whose English text names a condition the service does not produce (for example MSG-P3-032 "The service did not start" while readiness is DOWN and the process keeps running) is used verbatim from the Standard | Error and Message Standard v4 (source of record); spec §10.3 and CLAR-012 | `FixedMessageCatalog`, `ParameterStartupCheck` |
| IA-09 | The readiness indicator keeps only `messageCode` and the `{name, environment}` list in its details; the WARN line carries the Standard's English text per missing key | Spec SPEC-016, §12.9 | `ParameterStartupCheck` |
| IA-10 | A P4 `CatalogParameterReader` call maps a secret to `IllegalStateException` and "nothing in force" to `NoSuchElementException`, as the spec states, even though a P4 caller cannot see the P3 exception types | Spec §12.2 (finding 151) | `CatalogParameterReaderImpl` |
