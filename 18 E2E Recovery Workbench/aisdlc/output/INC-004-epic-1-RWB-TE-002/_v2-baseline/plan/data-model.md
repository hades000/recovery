# Data model — RWB-TE-002

No database, no entity and no migration. The data artefacts are the CODEOWNERS rule table, the branch
rule settings and the validation/test evidence.

## 1. CODEOWNERS rule table

| # | Pattern | Owner(s) | Purpose |
|---:|---|---|---|
| 1 | `/backend/src/main/java/th/co/scb/ace/demo/common/` | `@scb-ace/ace-team` | Common module main |
| 2 | `/backend/src/main/java/th/co/scb/ace/demo/recovery/` | `@scb-ace/techx-recovery-tech-leads` | Recovery main, including `generated.*` of TE-003 |
| 3 | `/backend/src/test/java/th/co/scb/ace/demo/recovery/` | `@scb-ace/techx-recovery-tech-leads` | Recovery test |
| 4 | `/backend/src/main/resources/db/modulemigration/recovery/` | `@scb-ace/techx-recovery-tech-leads` | Recovery migrations |
| 5 | `/frontend/src/modules/recovery/` | `@scb-ace/techx-recovery-tech-leads` | Recovery front end |
| 6 | `/backend/src/test/resources/architecture/recovery-modules.yaml` | `@scb-ace/techx-recovery-tech-leads` | Module map |
| 7 | `/.github/CODEOWNERS` | `@scb-ace/ace-team`, `@scb-ace/techx-recovery-tech-leads` | The file itself (BR4) |

Order: general first, specific last. The last matching pattern wins (BR5). No person, no email and no
personal data.

## 2. Branch rule settings

| Setting | `main` | `develop-recovery` | `develop` |
|---|---|---|---|
| Require a pull request | On | On | On |
| Require review from code owners | On | On | On |
| Required approvals | 1 | 1 | 1 |
| Dismiss stale approvals on a new commit | On | On | On |
| Author self-approval counts | No | No | No |
| Conversation resolution | Existing policy | Existing policy | Existing policy |

## 3. Validation result

| Field | Type | Meaning |
|---|---|---|
| `result` | `PASS` / `FAIL` | The pull-request check. |
| `line` | integer | The CODEOWNERS line. |
| `owner` | string | The team/user handle that failed, if any. |
| `pattern` | string | The pattern that matched no file, if any. |
| `reason` | string | `syntax`, `owner not found`, `no write access`, `pattern matches no file`, `duplicate pattern`. |

No token, no personal data and no file content are logged.

## 4. Test PR matrix

| Test | Path changed | Expected owner | Expected state |
|---|---|---|---|
| TC-TE-002-01 | Recovery Java fixture | Recovery team | Merge blocked until that team approves |
| TC-TE-002-02 | Common Java fixture | ACE team | ACE team requested |
| TC-TE-002-03 | One recovery + one common fixture | Both | Both approvals required |
| TC-TE-002-04 | Front-end + migration + module map | Recovery team | Recovery team for all three |
| TC-TE-002-05 | Recovery fixture, author is owner | Recovery team | Self-approval not counted |
| TC-TE-002-06 | Recovery fixture, new commit | Recovery team | Approval dismissed |
| TC-TE-002-07 | Recovery owner misspelt | — | Validation fails |
| TC-TE-002-08 | Recovery fixture, outside approver | Recovery team | Merge refused |
