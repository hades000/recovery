# Open items register

Items that need an owner outside the current agent run. One global register. IDs continue from the
carried register and are never reused. The v2 register keeps the items that are still open after the
15–16 November re-baseline and adds the new ones.

## Open

| ID | Item | Stories affected | Owner | Needed by | Raised in |
|---|---|---|---|---|---|
| OPEN-005 | Thai labels and messages are proposed (DL10) | All UI | BA Kuldeep | Before UAT | Decision Log v10 |
| OPEN-010 | Availability, RPO/RTO and retention are not signed | All | Product Owner / Compliance | Before SIT | NFR v3 |
| OPEN-016 | Per-story approver names are not in Jira | All | Product Owner | Before the next plan gate | Decision register |
| OPEN-017 | Add squad decisions D-RCV-34 and D-RCV-51/52 to the Decision Log | All | BA Kuldeep | Next Decision Log issue | `docs/decisions/decision-register.md` |
| OPEN-018 | Align the RWB-E1-044 story text with the Product Owner rulings of 9 Nov 2026 | RWB-E1-044 | BA Kuldeep | Next story issue | `docs/decisions/INC-001-decisions.md` |
| OPEN-019 | Jenkins Flyway job: second step with `db-migrate,db-migrate-recovery`, same DB role | Every recovery migration | Pongchai Charoenrungrodkun (K. Tee) | Before the first migration deploys | OPEN-013 ruling |
| OPEN-021 | Align RWB-TE-001 story text with D-RCV-36/37/39/42/52 | RWB-TE-001, RWB-E1-022 | BA Kuldeep | Next story issue | `docs/decisions/INC-001-decisions.md` |
| OPEN-024 | Name the real root and published packages of common and collection | RWB-TE-001 and callers | ACE team | Before the first cross-module call | D-RCV-41 |
| OPEN-026 | Confirm ACE build agents have Docker for `recoveryIntegrationTest` | Migration stories | Pongchai Charoenrungrodkun | Before recovery container tests join CI | D-RCV-44 |
| OPEN-028 | ACE tech lead checks the sample-module pattern for the recovery module | RWB-TE-001, RWB-E1-044 | Pipat Saengow | Before the build | Teams, 10 Nov 2026 |
| OPEN-031 | Context sync of D-RCV-50 (`develop-recovery` branch flow) | All | Context Updater | Done in this run | D-RCV-50 |
| OPEN-032 | Confirm AMIS, RPS, LIT, WIN, GL and COLLINS scores are ACE-ingested (D-RCV-35 §2.1) | RWB-E1-069 Section B, E2-006/018/019/021/027 | ACE team lead | Before the Section B views | D-RCV-35 |
| OPEN-033 | Confirm the final four extension-table names and keys against V0001 | RWB-E1-001, E1-069 | Data architect | Before V0001 merge | D-RCV-35 U3 |
| OPEN-034 | Pin the Temporal server and Java SDK versions; confirm 30-day retention | RWB-E1-070/071, E2-037–040 | SCB IT / Compliance | Before the Temporal build | ADR-011 |
| OPEN-035 | Confirm ACE Tier 1 tables are at the baseline head in DEV/SIT | RWB-E1-069 | ACE team | Before V0002 | E1-069 precondition |
| OPEN-036 | Re-baseline RWB-E1-044 and RWB-E1-043 specs/plans to schema `recovery` before build | RWB-E1-044, RWB-E1-043 | Technical Specifier / Planner | Before their build | L-RCV-05 |
| OPEN-037 | Name the product owner for the Epic 2 rule packages (RESTRUCTURE, PAYMENT_MATCH, BOOKING_MATCH) | E2-041/042 | RW-COE / RW-RISK | Before Epic 2 spec | D-RCV-36 T4 |
| OPEN-038 | Confirm the ACE repository host for RWB-TE-002 (GitHub-format `.github/CODEOWNERS` and branch rules, or GitLab equivalent), the real team handles/membership per DL37/DL36, the pipeline token scope, the protected branch names `main`, `develop-recovery`, `develop`, and whether a follow-up should add the common test folder (out of scope in this story). | RWB-TE-002 | ACE team repository administrator / recovery tech lead | Before TE-002 build | INC-004 spec CLAR-001..007; L-RCV-12/13 |
| OPEN-039 | Accept the RWB-TE-003 enforcement baseline (`L-RCV-11`), confirm `api/recovery-api.yaml` is the canonical copy of API Specification v4 (141 operations, 73 E1), approve the pinned generator/validator versions, and accept the P2 `generated.web`/`generated.model` packages (`L-RCV-14`). | RWB-TE-003 | Recovery tech lead / Forward Deployed Architect | Before TE-003 build | INC-005 spec CLAR-001..005; `L-RCV-11`, `L-RCV-14` |
| OPEN-040 | Run the live RWB-TE-003 access case `TC-TE-003-09` after RWB-E1-022 (SSO/roles) and RWB-E1-037 (permission matrix) exist; record 403, `application/problem+json`, `MSG-P4-002`. Until then the case is `BLOCKED`, not passed. | RWB-TE-003 | QA lead / recovery tech lead | Before the live access suite runs | INC-005 spec CLAR-006; D-RCV-52 |
| OPEN-041 | Close the canonical Story Defects v4 rows 91 (TE-002 BR4 vs §10), 92 (TE-003 lint checks omit x-module/x-first-release) and 93 (TE-003 pending vs no implementation) against the rulings in the INC-004/INC-005 runs; update the source document, not only the working copy. | RWB-TE-002, RWB-TE-003 | BA Kuldeep | Next document issue | INC-004/005 specs; L-RCV-11/13 |
| OPEN-042 | Confirm that the two E1 operations with `x-capability.area: None` (`getFeatureFlags`, `getMeSession`) are authentication-only and are reported `NOT_APPLICABLE_AUTHENTICATED`, or assign a real capability area in API Specification v4. | RWB-TE-003 | API owner / security administrator | Before the TE-003 lint gate | INC-005 spec CLAR-009; `ASM-TE003-09` |

## Settled in this baseline

| ID | Item | Ruling |
|---|---|---|
| OPEN-030 | Test dependency and shared-file edits for RWB-E1-044 | Approved with plan approval (D-RCV-49). |
| OPEN-027 | BR7 run before every MR | Confirmed by the Product Owner 10 Nov 2026; carried. |
| OPEN-029 | Context sync of D-RCV-44/47/48 | Superseded by the v2 context build; D-RCV-47 no longer applies. |
| OPEN-022 | Frontend import allow-list | Applied as FS-1.2 in `frontend-standards.md`. |
| OPEN-020 | DBA request for schema `recovery` | Reinstated by D-RCV-35 U3: the DBA creates schema `recovery` in SIT/UAT/PROD; the migration account holds DDL for the release window. |
| OPEN-025 | ACE core duplicate migration versions | Resolved upstream; no action. |
| OPEN-018 (PO part) | E1-044 BR7 and job-monitor deferral | CLAR-001 A and CLAR-002 A; story text update remains OPEN-018. |
| OPEN-023 | RWB-TE-001 build dependencies | Approved 9 Nov 2026. |
| OPEN-007 | Recovery Flyway on H2 | Skip recovery Flyway on H2; Testcontainers PostgreSQL for recovery tests. |
| OPEN-013 | How the recovery migration runs in SIT/UAT/PROD | Second Jenkins step with `db-migrate,db-migrate-recovery`. |
| OPEN-014 | Who creates schema `recovery` and holds DDL | DBA creates it; migration account holds DDL; application account has DML. Reinstated by D-RCV-35 (supersedes the 10 Nov withdrawal). |

## Notes

- D-RCV-47 (schema `ace`, `rwb_` prefix) is superseded. Any open item that referenced it is closed or
  restated above.
- No item on this register blocks the `RWB-E1-042` or `RWB-TE-001` specification/plan run.
- An item is closed by a dated ruling in the decision register, not by deleting the row.
