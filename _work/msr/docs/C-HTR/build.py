"""Build the full text of Recovery Workbench How To Read The Acceptance Criteria v2.

Every retained line, including its Thai text, is copied from the extracted source text
(_work/msr/extract/C-HTR/Recovery Workbench How To Read The Acceptance Criteria v1.md).
The new sections are inserted at fixed anchors, so the source order and wording survive.
"""
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
SRC = ROOT / "_work/msr/extract/C-HTR/Recovery Workbench How To Read The Acceptance Criteria v1.md"
OUT = ROOT / "_work/msr/docs/C-HTR/Recovery Workbench How To Read The Acceptance Criteria v2.md"

src = SRC.read_text(encoding="utf-8").splitlines()

def find(text):
    for i, line in enumerate(src):
        if line.strip() == text:
            return i
    raise SystemExit(f"anchor not found: {text}")

i_intro = find("Every user story ends in a set of acceptance criteria. They are the test the build must pass, and they are written to one pattern. Once you know the pattern, every story in the set reads the same way.")
i_three = find("A scenario has three parts")
i_patterns = find("The sentence patterns that repeat")

head = """SCB Collections and Recovery. Henka Group, 22 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

# Recovery Workbench

## How to read the acceptance criteria

SCB Collections and Recovery. Henka Group.

| Item | Detail |
|---|---|
| Document | Recovery Workbench how to read the acceptance criteria |
| Version | 2 |
| Date | 22 November 2026 |
| Supersedes | Version 1. The source gives no date and no status; the version is read from the file name (CG-C-HTR-1; ASM-C-HTR-1) |
| Prepared by | Henka Group |
| Applies to | Every reader of a Recovery Workbench story: the squads, the ACE team, the platform team, QA and the business |
| Decision | D-RCV-60: adopt Architecture v5 and realign the documents and stories |
| Status | Draft. No approval of this version is recorded (ASM-C-HTR-2) |
| Change | 2, 22 November 2026, D-RCV-60 microservice realignment, T3 Code / OpenCode / DeepSeek v4.1 Flash |

## Change log

| Version | Date | Change |
|---|---|---|
| 2 | 22 November 2026 | D-RCV-60 microservice realignment, T3 Code / OpenCode / DeepSeek v4.1 Flash. Adds How the set is sliced, The origin tag at the end of every scenario, The AC number inside the tag and Reading the slices of one legacy story, and extends A worked example and Where to read more. The sections A scenario has three parts, Every line states its own role, The result says who acts, The sentence patterns that repeat and The codes you will see are kept word for word with their Thai text |
| 1 | Not specified in the source documents (CG-C-HTR-1; ASM-C-HTR-1) | The reading pattern as issued: the three parts of a scenario, the role of each line, the actor in the result, one worked example, the repeating sentence patterns and the code prefixes. The source gives no version, date or status; the version is read from the file name (CG-C-HTR-1; ASM-C-HTR-1) |
"""

bridge = """
This version adds one idea to the pattern. A legacy story no longer maps to one story: it maps to a set of slices, one per service and work type, and every scenario now ends with a tag that says whether it comes from the legacy story or was added by the realignment. Four sections are new or extended for that: How the set is sliced, The origin tag at the end of every scenario, The AC number inside the tag and Reading the slices of one legacy story. The rest of the guide reads as it did.
"""

sliced = """## How the set is sliced

A story in this set is one slice of the work: the work one team type does for one service, and the smallest thing that can be built, tested and released on its own. A legacy story that asked several services to change becomes one story per service and work type, and each of those stories carries the acceptance criteria that belong to it. This version of the set holds 1,034 slices over 358 keys, 341 of them legacy stories and 17 new, and the slices fall into 288 contract stories, 513 app development stories, 11 ACE DB stories, 18 infrastructure stories, 57 DevOps stories and 147 integration stories (CG-C-HTR-4; ASM-C-HTR-4).

A story key says which slice you are reading. It has four parts, and a fifth for the delta copy of a preserved story.

| Part | Values | Example |
|---|---|---|
| RWB | Always RWB | RWB |
| Scope | P1 to P10 and S1 to S9 for the 19 services, PLT for a platform epic, ITG for an integration epic | ITG |
| Legacy compact | The legacy key without its dashes: E1001 for RWB-E1-001, TE001 for RWB-TE-001, AD003 for RWB-AD-003. N001 onwards is a new platform story and W1J01 the new integration harness | E1001 |
| Work type | CON, APP, DB, INF, OPS or ITG | ITG |
| -2 | The delta copy of a preserved story; the copy without -2 stays the as-built story | -2 |

So RWB-P3-E1018-APP is the app development slice of RWB-E1-018 on rwb-case, and RWB-PLT-TE001-APP is the preserved technical enabler RWB-TE-001 with RWB-PLT-TE001-APP-2 as its delta. A reader who knows the legacy key can find every slice of it from its key.

| Work type | Key ends | What the slice proves | Suggested owner |
|---|---|---|---|
| Contract | -CON | What the service publishes and consumes: the request, the response, the event, the error and the timeout. A contract story is always Day 1 and has no build dependency | TechX (suggested; any team may pick up this story) |
| App development | -APP | The behaviour inside one service, built against the contract stories and their fakes | TechX (suggested; any team may pick up this story) |
| ACE DB | -DB | The service's own schema, its migration and its grants | ACE team (suggested; any team may pick up this story) |
| Infrastructure | -INF | The environment, the database instance and the deployment the service needs | SCB IT infrastructure (suggested; any team may pick up this story) |
| DevOps | -OPS | The pipeline, the monitoring and the run tasks of the service | DevOps team (suggested; any team may pick up this story) |
| Integration | -ITG | The real cross-service behaviour: two or more services, the topic and the workflow. Integration dependencies sit only here | TechX (suggested; any team may pick up this story); a harness or NFR story reads QA team (suggested; any team may pick up this story) |

RWB-E1-001, the story that creates the recovery tables, is one legacy story and five slices: RWB-P1-E1001-APP on rwb-source-data, RWB-P7-E1001-APP on rwb-decision, RWB-P4-E1001-APP on rwb-access, RWB-P8-E1001-APP on rwb-payment and RWB-ITG-E1001-ITG across them. Read the five together as one story whose criteria have been sorted by owner.

Six stories are kept word for word, because they are built or in build: RWB-TE-001, RWB-TE-002, RWB-TE-003, RWB-E1-042, RWB-E1-043 and RWB-E1-044. The slice with the base key holds the legacy text as built, and the microservice change sits in the -2 copy or in a platform contract or DevOps story. In a preserved story sections 1 to 11, 14 to 16, 18 and 19 are the as-built text, and sections 12 and 13 are marked as the monolith.

"""

worked_note = """In this version the same scenario sits in RWB-ITG-E1001-ITG, the integration slice of RWB-E1-001. The scenario line keeps its number, AC7, and adds the origin tag at the end: (legacy RWB-E1-001 AC7). The table above reads exactly as it did.
"""

tagged = """## The origin tag at the end of every scenario

Every scenario starts with Scenario, the number of the criterion and a short name, and ends with the origin in brackets. The tag answers one question: was this line promised before the realignment, or is it new? There are only two tags.

| Tag | Written like this | What it tells you |
|---|---|---|
| Legacy origin | (legacy RWB-E1-001 AC7) | The scenario is AC7 of RWB-E1-001 and was written before the realignment. Its meaning is unchanged; only the actor and the sentence shape follow the pattern above. AC7 is the same scenario in every place it appears |
| New origin | (new, D-RCV-60) | The scenario was added by the realignment and has no earlier text. The line is the whole requirement, and there is nothing older to compare it with |

Nothing else ends a scenario. A line with no tag, or with a third kind of tag, is a defect in the story and is raised against the story key.

## The AC number inside the tag

A story numbers its scenarios AC1, AC2 and so on. A scenario taken from a legacy story keeps the number it has there, so the numbers in a slice can have gaps. In RWB-ITG-E1001-ITG the inherited scenarios are AC2, AC3 and AC7; AC1 and AC4 to AC11 are in RWB-P1-E1001-APP. The gap is the reading help: it shows that another slice of the same legacy story owns the missing numbers, and that ACn names one scenario and is not a count.

A new scenario takes the next free number in its story. In RWB-ITG-E1001-ITG the new scenarios are AC12 to AC15, after AC11, the last number of RWB-E1-001. A story with no legacy ancestor starts at AC1, and every one of its scenarios is new.

| The line starts | The tag | The reading |
|---|---|---|
| Scenario: AC2 Dictionary published | (legacy RWB-E1-001 AC2) | Inherited from the legacy story, with its number and its meaning |
| Scenario: AC7 Catalog row with two systems of record is refused | (legacy RWB-E1-001 AC7) | The worked example above, in the story that carries it now |
| Scenario: AC12 Every one of the 92 tables resolves to exactly one owning schema | (new, D-RCV-60) | Added by the realignment; there is no legacy text for it |
| Scenario: AC15 The same catalog file loaded twice writes nothing the second time | (new, D-RCV-60) | Added by the realignment, and numbered after the last legacy number |

## Reading the slices of one legacy story

Read the slices of a legacy story in the order a service needs them: the contract stories first, because they are Day 1 and everything else builds against them; then the app development, DB, infrastructure and DevOps slices of each service; then the integration story, which is the only place the real cross-service behaviour is proven. RWB-E1-001 has no contract story; its five slices are four app development stories and one integration story.

| Slice | Work type | Legacy scenarios it carries | New scenarios |
|---|---|---|---|
| RWB-P1-E1001-APP | APP | AC1, AC4, AC5, AC6, AC8, AC9, AC10, AC11 | None |
| RWB-P4-E1001-APP | APP | None, the five authority tables are new work | AC1 to AC11 |
| RWB-P7-E1001-APP | APP | None, the six decision and rules tables are new work | AC1 to AC11 |
| RWB-P8-E1001-APP | APP | None, the proceeds table is new work | AC1 to AC11 |
| RWB-ITG-E1001-ITG | ITG | AC2, AC3, AC7 | AC12 to AC15 |

The count is the check. RWB-E1-001 has 11 legacy scenarios, the table accounts for all 11, one slice each, and the 37 new scenarios are added around them. When two slices of one legacy story claim the same ACn, the set is wrong and the story key is raised.

"""

tail = """
Every slice is listed with its work type, its wave and its release in the Service Story Catalog v1, and the Legacy map sheet of that file names the new stories for every legacy key, so a reader who starts from a legacy key can find every slice of it. The Story Build Order v3 gives the order the slices are built in, the Day-1 Work Allocation v1 names the work that can start on the first day, and the Dependency Map v4 shows which story waits for which.

The four new sections, How the set is sliced, The origin tag at the end of every scenario, The AC number inside the tag and Reading the slices of one legacy story, are written in English. The Thai reading of them is not specified in the source documents (CG-C-HTR-3; ASM-C-HTR-3).
"""

lines = head.splitlines()
lines += [""]
lines += src[i_intro:i_three]

def trim(block):
    while block and not block[-1].strip():
        block = block[:-1]
    return block

lines = trim(lines)
lines += bridge.splitlines()
lines += [""]
lines += sliced.splitlines()
lines += src[i_three:i_patterns]
lines = trim(lines)
lines += [""]
lines += worked_note.splitlines()
lines += [""]
lines += tagged.splitlines()
lines += src[i_patterns:]
lines += tail.splitlines()

# The source sets its section names as plain paragraphs; give each one a heading level
# so the new version navigates like the rest of the set. The wording is not touched.
HEADINGS = {
    "A scenario has three parts": "## ",
    "Every line states its own role": "## ",
    "The result says who acts": "## ",
    "A worked example": "## ",
    "The sentence patterns that repeat": "## ",
    "The codes you will see": "## ",
    "Where to read more": "## ",
}
lines = [HEADINGS.get(l.strip(), "") + l if l.strip() in HEADINGS else l for l in lines]

OUT.write_text("\n".join(lines).rstrip() + "\n", encoding="utf-8")
print("WROTE", OUT, len(lines), "lines")
