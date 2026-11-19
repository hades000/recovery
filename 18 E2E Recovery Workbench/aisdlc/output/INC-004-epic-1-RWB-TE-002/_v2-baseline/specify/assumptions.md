# Assumptions — RWB-TE-002 specification

| ID | Assumption | Basis | Effect if wrong |
|---|---|---|---|
| `ASM-TE002-01` | The ACE repository host is GitHub-compatible: `.github/CODEOWNERS`, branch rule on `main`, code-owner review. | Story §3, §12; DL37. | If GitLab, use `.gitlab/CODEOWNERS` and protected-branch approval rules. `OPEN-038`. |
| `ASM-TE002-02` | Story paths are placeholders; the actual paths are the TE-001 layout. | RWB-TE-001; D-RCV-02/10/37. | A stale path leaves a folder unowned; the pattern-match check catches a pattern with no file. |
| `ASM-TE002-03` | Recovery code-owner team `@scb-ace/techx-recovery-tech-leads` includes the tech lead and squad developers; ACE team is `@scb-ace/ace-team`. | D-RCV-21; story §3. | Handles change; membership stays the control. |
| `ASM-TE002-04` | Branch rule applies to `main`, `develop-recovery` and `develop`. | Story §12; D-RCV-50. | A missed branch lets a recovery MR bypass review. |
| `ASM-TE002-05` | Common test folder is out of scope; a follow-up adds it once it exists. | BR3; story §12; pattern-match validation. | A common test change is not code-owned until the follow-up; `OPEN-038` records it. |
| `ASM-TE002-06` | The pipeline token can read organisation teams and repository permission, or a service token is provisioned. | Story §12. | The validation fails closed; `OPEN-038` names the owner. |
| `ASM-TE002-07` | BR4 wins: the CODEOWNERS file is owned by both teams; §10's ACE-team right is the branch rule. | Story defect row 91; BR4. | One team could change the other's ownership without consent. |
| `L-RCV-03` | No question was asked; the host, path and team-name ambiguities are recorded here and in `OPEN-038`. | No-question rule. | A wrong default is visible at the plan gate. |

No question was asked. Items that need a human owner are in `docs/open-items.md` (`OPEN-038`, `OPEN-041`).
