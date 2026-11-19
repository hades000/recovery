# Assumptions — RWB-TE-002 plan

| ID | Assumption | Basis | Effect if wrong |
|---|---|---|---|
| `ASM-TE002-01` | GitHub-compatible host; `.github/CODEOWNERS` and code-owner branch rules. | Story §3/§12; DL37. | Use `.gitlab/CODEOWNERS` and protected-branch approval rules; `OPEN-038`. |
| `ASM-TE002-02` | Actual TE-001 paths replace the story placeholders. | RWB-TE-001; D-RCV-02/10/37. | A stale path is caught by the pattern-match check. |
| `ASM-TE002-03` | Recovery team membership includes the tech lead and squad developers; handles are values. | D-RCV-21; DL37/DL36. | A reviewed file change updates the handle/membership. |
| `ASM-TE002-04` | The branch rule applies to `main`, `develop-recovery` and `develop`. | Story §12; D-RCV-50. | A missed branch lets a recovery MR bypass review. |
| `ASM-TE002-05` | The common test folder is out of scope; a follow-up adds it once it exists. | BR3; story §12; pattern-match validation. | A common test change is not code-owned until the follow-up; `OPEN-038` records it. |
| `ASM-TE002-06` | The pipeline token can read teams and permission, or a service token is provisioned. | Story §12. | The step fails closed; PRE-4 blocks the build. |
| `ASM-TE002-07` | BR4 wins over §10; the file is owned by both teams. | Story defect row 91; BR4. | One team could change the other's ownership. |
| `L-RCV-03` | No question was asked. | No-question rule. | A wrong default is visible at the plan gate. |

No question was asked. The open item is `OPEN-038` (host, teams, token, branches) and `OPEN-041`
(canonical defect-register closure).
