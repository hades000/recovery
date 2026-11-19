# Host configuration record: RWB-TE-002 code owners

Status: `OPEN — NOT_APPLIED_HERE`. No ACE GitLab host is connected in this run (RUN-BRIEF hard rule 5).

Owner of every row: the ACE team repository administrator with the recovery tech lead (story §3, §4 step 3; D-RCV-50). Apply HC-01..HC-09 on the ACE GitLab project, then run HV-01..HV-11 and record the MR link and result for each item. No row is applied here; no HV item is passed.

GitLab setting names are the specifier's mapping of story §12 under L-RCV-12 (ASM-TE002-10). The administrator confirms each name on the target tier (OPEN-038).

| ID | GitLab setting | Value | Branches | Source | Verified by |
|---|---|---|---|---|---|
| HC-01 | Repository > Protected branches: allowed to push and merge | No one (changes arrive by MR) | `main`, `develop-recovery`, `develop` | Story §12 "Require a pull request"; L-RCV-13 | HV-01 |
| HC-02 | Protected branch: code owner approval required | On | Same | Story §12 "require review from code owners"; BR6 | HV-01, HV-03 |
| HC-03 | Merge request approvals: required approvals | 1 | Same | Story §12 "1 approval" | HV-01 |
| HC-04 | Approval settings: prevent approval by author | On | Project | Story §12 "the author's approval does not count"; AC5 | HV-04 |
| HC-05 | Approval settings: when a commit is added, remove all approvals | On | Project | Story §12 "dismiss stale approvals"; AC6 | HV-05 |
| HC-06 | Merge checks: pipelines must succeed | On | Project | Story §4 step 6 (a failed check blocks); Engineering Practices v5 §7 gates block merge | HV-07 |
| HC-07 | Default MR description template | `Default` | Project | SPEC-015; A-10 | HV-09 |
| HC-08 | Groups for every `ASSUMED` handle exist with at least write (Developer) access to the project; `PLACEHOLDER` handles replaced first | Per register | Project | Story §12 "every owner exists and has write access"; §3 | HV-07, HV-11 |
| HC-09 | Settings > CI/CD > General pipelines: use separate caches for protected branches | On | Project | Security review F8 and code gate CODE1-002 (a distinct cache key alone does not stop an unprotected-branch pipeline writing the `gradle-codeowners` cache); D-RUN-25 addendum, **not in the spec or story**: ratification by the tech lead pending (IM-SU-04) | HV-07 |

"Allowed to merge" roles are not set by this story: D-RCV-50 and Engineering Practices v5 §4.2 decide who merges; the administrator applies them.
