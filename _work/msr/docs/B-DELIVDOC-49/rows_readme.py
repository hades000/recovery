"""Builds the rows JSON for the Read me sheet of Resource Plan v3 (scratch, B-DELIVDOC-49)."""
import json
from pathlib import Path

OUT = Path(__file__).resolve().parent
P = "CG-B-DELIVDOC-49-{}".format
A = "ASM-B-DELIVDOC-49-{}".format
PH = lambda n: f"Not specified in the source documents ({P(n)}; {A(n)})"

rows = [
    ["SCB Collections and Recovery. Henka Group, 22 November 2026."],
    ["(C) Siam Commercial Bank and Henka Pte Ltd"],
    ["Recovery Workbench Resource Plan and Team Structure v3 (D-RCV-60)."],
    ["Who is on the programme, the people by month, the team structure and the run accountability, in the 19-service shape. "
     "Suggested ownership is by team type only; any team may pick up a story. Every release date is tentative (DL48)."],
    ["Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash."],
    [f"Version 3; 22 November 2026; Status Draft (no approval recorded; {P(11)}; {A(11)})."],
    [],
    ["Change log"],
    ["Version", "Date", "Change", "Tool"],
    ["v2", f"Not stated in the source workbook ({P(1)}; {A(1)})",
     "Source version. Four sheets kept word for word: Team, People by month, Structure, Accountability. "
     "Counts for TechX follow the assumed squad shape until the named team is confirmed (DL36).",
     "Not recorded in the source"],
    ["v3", "22 November 2026", "D-RCV-60 microservice realignment", "T3 Code / OpenCode / DeepSeek v4.1 Flash"],
    ["Change log row: v3, 22 November 2026, D-RCV-60 microservice realignment, T3 Code / OpenCode / DeepSeek v4.1 Flash"],
    [],
    ["What version 3 changes"],
    ["- The four sheets of version 2 keep every section, ID, number and date: the 24 team rows with their From and To dates "
     "(Sep 2026, Nov 2026, Feb 2027, Mar 2027 and Jun 2027), the 20 people-by-month rows with the Total row formulas, "
     "the 6 structure rows and the 11 accountability rows. No row of those four sheets is edited."],
    ["- Suggested ownership by team type is added on the Ownership by team type sheet: the six work types of Template and Rules "
     "R5.3 with their fixed owner phrases, what the owner holds in the 19-service shape, and the Day-1 rule of R5.7 rule 6."],
    ["- Artefact ownership is added on the same sheet from the Ownership Map v1: parameters and reference data P3 rwb-case, "
     "the case list API P3, the rule package registry P7 rwb-decision, the interaction ledger P1 rwb-source-data, feature flags the "
     "platform library, the workflow kit the platform team, and one schema and login per service with the ACE team."],
    ["- The 19 services are put against the wave of the Ownership Map v1 Services sheet, the module named for them in the Structure "
     "sheet and the squad that carries that module, with the story volume of each service from the plan (Services and squads)."],
    ["- Team-type coverage is put against the people the plan records (Team types and resources): TechX 12 full-time equivalents "
     "across the two squads, ACE team 1, QA 2 inside TechX and not counted twice, the 9.5 program and 7 data and business roles "
     "that belong to no team type of R5.3, and the 29.5 full-time equivalents of the Total row. The team types with no "
     "full-time equivalent are named there, not invented."],
    [f"- The wave 0 platform epics have no team, no full-time equivalent and no accountable role in version 2 ({P(4)}; {A(4)}); "
     "the column that would hold them is left at the R9 placeholder."],
    ["- No person is named anywhere (AGENTS.md rule 4). Owners are service codes of the Ownership Map v1 and team types only. "
     f"The module wording of the structure and accountability rows is kept word for word, and the service-level reading is "
     f"stated next to it instead of editing the rows ({P(9)}; {A(9)})."],
    ["- Every release date is unchanged and tentative (DL48; Template and Rules U7). No date was raised as a gap."],
    [],
    ["Sheets in this version"],
    ["Sheet", "What it holds", "New in v3", "Source"],
    ["Read me", "Header, version, status, change log and what changed", "All of it", "Template and Rules R8.1"],
    ["Team", "The 24 rows who is on the programme, with role, organisation, people, From and To, accountability and status",
     "Nothing: kept word for word", "Version 2"],
    ["People by month", "Full-time equivalents by role and month, November 2026 to June 2027, with the Total row",
     "Nothing: kept word for word", "Version 2"],
    ["Structure", "Programme, two recovery squads, ACE team, Collection squad and supporting teams",
     "Nothing: kept word for word", "Version 2"],
    ["Accountability", "The 11 items and the one role accountable for each",
     "Nothing: kept word for word", "Version 2"],
    ["Ownership by team type", "The six work types with their suggested owners, what each owner holds, the Day-1 rule, "
     "and artefact ownership from the Ownership Map v1", "All of it", "Template and Rules R5.3, R5.7, R3; Ownership Map v1"],
    ["Services and squads", "The 19 services with wave, source module, squad, the owner by work type and the story volume",
     "All of it", "Ownership Map v1 Services sheet; version 2 Structure; plan legacy and stats"],
    ["Team types and resources", "The five team types and the other role rows against the full-time equivalents of the People by "
     "month sheet, and what the plan does not staff", "All of it",
     "Version 2 People by month and Structure; Template and Rules R5.3"],
]

(OUT / "rows_readme.json").write_text(json.dumps(rows, ensure_ascii=False, indent=1), encoding="utf-8")
print("rows", len(rows), "placeholder check", PH(1))
