# Post-merge evidence audit: RWB-E1-044, RWB-TE-001, RWB-E1-042, RWB-TE-002

| Field | Value |
|---|---|
| Audited | `develop-recovery` at `27567ed`, plus the uncommitted log and shared-file edits of 18 Nov evening |
| Auditor | Independent review agent (Claude Opus 5.5, high effort), read only, briefed to act as a sceptical bank reviewer |
| Question | Would a bank reviewer find gaps in the evidence that the four stories were built with the AISDLC playbook, or find contradictions in that evidence? |
| Disposition | `README.md` in this folder gives the fix or registration for each finding |

> Provenance: the agent returned this report as text, and the orchestrator saved it here in condensed form.
> The IDs, locations and fixes are unchanged.

## High

| ID | Where | Finding | Recommended fix |
|---|---|---|---|
| H-01 | AGENTS.md §1.4, §8, §9; the four merge commits; OPEN-016 | The four merges have no named human reviewer or approver. OPEN-016 is still open | The tech lead or reviewer records their own approval, or the repository says plainly that the four merges are AI-reviewed and waiting for human approval |
| H-02 | `aisdlc/SOURCES.md` vs CLAUDE.md:18 | SOURCES.md has only a header row, yet CLAUDE.md says it lists every source with a SHA-256 | Fill it from the document-set baseline, or point CLAUDE.md elsewhere |
| H-03 | Log header; row 420; commits from 18 Nov 07:19 to 18:57; `0b87102`, `6c03afa`, `029f578` | The tool and model changes are not declared. Some commit trailers name a tool or model that did not write the commit | Add a decision row and correction rows that list the affected commits. Correct the header's tool row |
| H-04 | AGENTS.md §11 | The table says "No entries yet", although reviewers found AI errors (TE-001 Thai mojibake, E1-042 PLAN-001 and CODE-001, TE-002 F1/F2, E1-044 code-gate Lows) | Add one dated row per error |
| H-05 | Log header, sections 2 to 4 | The header claims ten stories. Sections 2 and 3 are empty, and section 4 says "to be completed". There is no decision row for the stop after four | Restate the scope. Add a decision row for the stop. Fill sections 2 to 4 |
| H-06 | Log | These stages have no log rows: E1-044 implement start, pre-merge review rounds, API and functional tests; TE-001 API and functional tests; E1-042 and TE-002 implement start and documentation. The E1-044 code-gate rounds are folded into one row | Add Log correction rows with the true times |
| H-07 | E1-044, TE-001 | The documentation was written after the code gate passed | (See README: the playbook's Technical Documenter runs the code gate *before* it writes the docs, so this order is by design) |
| H-08 | INC-003 README:27 | The README names traceability-manager, but the orchestrator did that stage | Correct the README and add a correction row |
| H-09 | `Traceability_Matrix.md` sections 6 to 8 | Stale counts, a `<merge SHA>` placeholder, and rows that still say they "wait for" merges that are done. `TRACEABILITY_STATUS: CURRENT` is false | Update the sections |
| H-10 | INC-001 `docs/COMPLIANCE.md:149-150`; INC-004 `code-gate-review.md:45`; INC-001 code-gate verdict text | Wording that reads as risks or Lows "accepted" by the AI | Reword them as open for tech-lead acceptance, and add notes to the gate files |

## Medium

| ID | Finding |
|---|---|
| M-01 | INDEX.md rows 006 to 010 and the note at line 94 are stale against the log |
| M-02 | README.md: the layout section, "coverage verification not part of check" and "V0001-V0003 from RWB-E1-001" are false |
| M-03 | The E1-044 spec gates have no `SPEC_GATE:` line, only "Overall: PASS" |
| M-04 | Hardening commit `e566360` changed a test directly on `develop-recovery`, with no branch, gate or review |
| M-05 | Log row 72 "Plan approved / Engagement lead / APPROVED" was written by the orchestrator. D-RUN-24 says "the lead has accepted". D-RUN-16 says "approved spec, plan" |
| M-06 | D-RUN-23 has time 11:50, but its timeline row has 11:44:35 |
| M-07 | INC-003 and INC-004 README line 12 name no merge SHA |
| M-08 | Commit author is a personal gmail. 129 tracked logs contain `C:\Users\<user>` paths. open-items.md names individual client staff |
| M-09 | Open items marked "before build" are still open (OPEN-028, OPEN-036). OPEN-031 is done but listed as open. OPEN-033 and OPEN-035 use stale V-numbers |
| M-10 | There is no ratification item for D-RUN-07, D-RUN-10..13, D-RUN-15 or D-RUN-17 (only D-RUN-14 has one) |
| M-11 | DOCUMENT-GAPS.md holds only DG-001..005. The per-story gaps were left for an end consolidation pass that this run will not reach |
| M-12 | The E1-042 API contract test lives only under `api-tests/` and runs through an init script. The report header cites run 4, but run 5 is current |
| M-13 | The "unknown second writer" raised in log row 437 was never resolved |
| M-14 | CLAUDE.md claims the evidence does not support: there is no end hash of the document set; it says "a human starts each stage"; it says every review round has its own file; it says every commit has a Plan trailer |

## Low

| ID | Finding |
|---|---|
| L-01 | INC-002 README: wrong commit count, pre-rebase SHAs, A-1..A-4 vs A-1..A-3, merge time |
| L-02 | INC-001 README: OPEN-050 should be OPEN-051; implement start and merge times; fixture count drift |
| L-03 | `27567ed` has `AISDLC-Stage: implement` and says the post-merge suites "are logged" |
| L-04 | spec-gate-review-7 cites a build-log row by line number |
| L-05 | `8675a5c` has trailers that git cannot parse. `615d9ee` has `AISDLC-Run: multiple` |
| L-06 | E1-042 has both report.md and implementation-report.md; TE-002 has no unit-tests report; the addendum is in a different place per story; there is a stray `spec.pre-build-status.md` |
| L-07 | There are 550 `*.runN.*` backup files and no explanation of the convention |
| L-08 | Script name in DG-004; dash style in rows 79-80; TC-E1-042-12 deferred with no open item; DEV-09 not in AGENTS §11 |
| L-09 | `.env.example` holds the Azurite AccountKey. It is the public emulator key, but a scanner will flag it |

## Solid (as reported)

- Every gate count in the log matches the gate file, for every round of all four stories, and every final gate is PASS.
- Every evidence path cited in matrix rows 001 to 004 and in the run READMEs exists.
- Every story-branch commit carries `AISDLC-Run`, `AISDLC-Stage` and `AISDLC-Plan`.
- Merge commits carry the plan, the tool, the test results and the OPEN-016 note.
- Red/green logs exist for every task.
- D-RUN-09 is applied consistently, and log corrections are append-only.
- There is one migration, V0001, with a correct header.
- There are 12 agents and 5 commands, as CLAUDE.md states.
- The disclosures are honest: opencode use, DEV-09/DEV-10, harness provenance notes, the security review done by hand, and HV-01..11 marked "not tested".
