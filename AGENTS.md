# Realignment run rules (D-RCV-60). Read before any work in this folder.

Decision ID for every new file: **D-RCV-60** (allocated by A5 because D-RCV-53 is already used in folder 21). The plan draft calls it D-RCV-53; use D-RCV-60 in every output.

Tool and model: T3 Code / OpenCode / DeepSeek v4.1 Flash. Never write a Claude or other tool trailer.

1. Never edit a file that already exists. Copy it to the next version and edit the copy. Edit only the files your WP lists under "Write only".
2. Read-only: folders "17 AI-First SDLC Repository v2", "18 E2E Recovery Workbench", "21 Jira Export E2E Workbench", and everything else not listed as an output.
3. No external writes: never call Jira, Confluence, GitLab, Figma or the web. No git commits.
4. No names of people anywhere. Use roles only.
5. Scratch area: _work/msr/ (wp, plan, extract, fragments, gaps, assumptions, editlog, logs, smoke, probe, status.json).
6. A story WP writes only: its story files; _work/msr/fragments/<story-id>.json; _work/msr/gaps/<WP>.jsonl; _work/msr/assumptions/<WP>.jsonl; _work/msr/editlog/<WP>.md.
7. Only the assembler (Stage C) writes master files. Only step D1 numbers gaps (GAP-nnnn) and assumptions (ASM-nnnn).
8. Never invent a value. Write "Not specified in the source documents (CG-<WP>-<n>; ASM-<WP>-<n>)" and add a jsonl row. Copy numbers and IDs character for character.
9. Never ask the user anything and never wait for approval. Missing approval or status: record an ASM and continue in Draft status.
10. Dates: copy unchanged; mark every release date "(tentative)". Never raise a date as a gap.
11. Run Python as: python -I "<absolute or ROOT-relative script path>" <args>. No cd chains.
12. Before returning: python -I "22 Microservice Realignment/checks/run_all.py" --wp <WP> --quick ; fix every failure; rerun.
13. If something fails after 3 tries, write it to the edit log as FAILED with the reason and return. Never stop the run.
14. Parallel work: when your WP says "fanout: F", delegate one legacy story per task subagent (agent aisdlc-msr-worker), up to F at once, in one message with several task calls. Never fewer than the WP allows.
