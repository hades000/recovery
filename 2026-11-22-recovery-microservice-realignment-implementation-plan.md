# Recovery Workbench Microservice Realignment Implementation Plan

> **For agentic workers.** This header replaces the writing-plans default, at the user's request.
> - **Do not** use superpowers:subagent-driven-development.
> - **Do not** use superpowers:executing-plans checkpoints.
> - **Do not** make one-task-at-a-time human review stops.
> - **Do not** make commits.
>
> **REQUIRED SUB-SKILL: superpowers:dispatching-parallel-agents.** Apply it at the largest scale the provider allows:
> - Tasks 1–18 build the tools and run in order, in one coordinator session. Tasks 11 and 17 already fan out their small queues through `run_parallel.py`.
> - Tasks 19–21 dispatch every independent work package at once through `run_parallel.py`.
> - Concurrency comes from the **measured** capacity (Task 6), never from a fixed small number.
> - Never lower the concurrency to "be safe". Lower it only when `run_parallel.py` sees a rate-limit or quota signal.
>
> Steps use checkbox (`- [ ]`) syntax. Tick them in this file as you go.

**Goal:** Produce the new version of the Recovery Workbench document set and every epic and story, realigned to the 19-service architecture of `Proposed Arch/Recovery Microservice Architecture v5.pptx`. Output is per-service epics, parallel lanes and team-type slices, so that every team can start work the next day. Also produce the BRD/PRD versions, separate Gap and Assumptions registers, a Jira impact file, and one large Excalidraw architecture diagram.

**Architecture:**
1. Python scripts (stdlib plus openpyxl, python-docx, python-pptx, networkx, yaml) do every deterministic step: convert, index, classify, split, lane, check, number, assemble, draw.
2. DeepSeek v4.1 Flash agents, run through OpenCode from T3 Code, do the writing. Each agent gets one self-contained work package (WP) file, covering at most 5 legacy stories or one document family.
3. A weighted-semaphore runner keeps the measured maximum number of model sessions busy at all times, and pauses only on provider quota.

**Tech Stack:**
- Python 3.11.9, used as `python -I`. pytest is **not** installed; use `unittest`.
- openpyxl, python-docx, python-pptx, networkx, PyYAML.
- OpenCode v2.3.2, run as `opencode run --agent … --model …`. Model `opencode-go/deepseek-v4.1-flash`, variant `max`.
- T3 Code, through its OpenCode provider.
- Excalidraw v2 JSON.

**Working folder (ROOT):** `C:\Users\SahilMore\Downloads\Recovery Workbench SharePoint Set v14\`. Every relative path in this plan is relative to ROOT. A copy of this plan is saved as `ROOT\2026-11-22-recovery-microservice-realignment-implementation-plan.md`.

---

## 0. Execution mode (read before Task 1)

### 0.1 How this plan overrides the writing-plans defaults

| writing-plans default | This run |
|---|---|
| Use subagent-driven-development, sequential with review between tasks | **No.** Tasks 1–18 are built by one coordinator in order. Tasks 19–21 fan out everything at once. |
| Executing-plans checkpoints for human review | **No human stops.** Never ask the user. Record an assumption and continue (AGENTS.md rule 9). |
| Frequent commits | **No commits** (rule 3). A step that would commit runs the tests again instead. |
| Save to `docs/superpowers/plans/` | Saved at ROOT, as the user asked. |
| One sub-agent per problem domain | Kept. One WP = one domain (≤5 legacy stories, or one document family). The **number running at once** is the measured maximum, not 3. |

### 0.2 Measured capacity for `opencode-go/deepseek-v4.1-flash`

The measurements were taken on 21–22 Nov 2026 by read-only queries on `~/.local/share/opencode/opencode.db` (table `session_v2`, children counted by `parent_id`) and on `~/.local/share/opencode/log/opencode.log`.

| Fact | Value |
|---|---|
| Most task subagents running at once inside one OpenCode session | **10** (23 Oct 2026, 19 children, agent `general`) |
| The 18 Nov Recovery Workbench AI-SDLC run | 7 at once, 78 children |
| Most deepseek-v4.1-flash sessions running at once, machine-wide (parents plus children) | **19** |
| HTTP 429 or rate-limit lines in about 120 000 log lines | **0** |
| OpenCode Go usage windows on 21 Nov, from `~/.t3/caches/opencode.json` → `usageLimits.windows` | Session (300 min): 0 % used. Weekly: 44 %. Monthly: 56 %. |

These are lower bounds, not limits: no earlier run tried more. **Task 6** ramps a live probe to find the real ceiling, then writes `_work/msr/plan/capacity.json`.

**Defaults if the probe cannot run:**
- `budget = 19` live model sessions.
- `fanout = 5` task subagents per story WP.

### 0.3 How the budget is spent

`run_parallel.py` holds one counter, `budget`: the number of model sessions allowed to be live at once.

- **Weight of a WP.** A plain WP costs 1. A story WP that delegates one task subagent per legacy story costs `1 + fanout`.
- **Scheduling.** The runner starts the next WP from the queue whenever enough budget is free, so the budget is always full.
- **Quota.** If any OpenCode Go window reaches 90 % or more, the runner stops launching. For the session window it waits until `resetsAt`. For the weekly or monthly window it writes `PAUSED_QUOTA` and exits with code 3. Rerun the same command after the reset: DONE WPs are skipped.
- **Rate limits.** On a 429 or 5xx it backs off for 30 s, then 2 min, then 5 min, and lowers `budget` by 2 (the floor is 4). After 10 minutes clean, it raises the budget again by 1, up to the probe value.

---

## 1. Context

**Why this run exists.**

The architecture team's v5 target (20 Nov 2026) replaces the modular monolith. The v5 target has:
- 19 services `rwb-<short>`, all inside ACE;
- one ACE PostgreSQL schema `rwb_<name>` and one login per service;
- Kafka with outbox and inbox;
- a reusable Temporal layer, where Schedules replace Quartz;
- embedded Drools;
- no data lake;
- Waves 0 to 4.

The detailed Temporal and Drools design is in `Proposed Arch/Recovery Temporal and Drools Detailed Design v1.pptx`.

Document set v14 still assumes the monolith:
- ADR-002, one service;
- one `recovery` schema with 92 tables;
- one Flyway sequence;
- one `api/recovery-api.yaml`;
- in-process calls;
- one decision-log writer (E1-027);
- Quartz.

Because of this, Epic 1 forms one serial chain of 194 dependency links, and the infrastructure, DevOps and ACE DB work is hidden inside TechX stories.

**Intended outcome:**
- 31 epics: 7 platform, 19 service, and 5 integration.
- Stories inside each epic are split into parallel lanes of depth 4 or less.
- Separate linked stories per team type, each with a *suggested* owner only.
- Day-1 work for every team type.
- New versions of every affected document.
- Separate, versioned Gap and Assumptions registers.
- A Jira impact file. Jira is never touched.
- One large technical Excalidraw diagram, by epic and story.

**User decisions** (fixed; full text in Appendix R §R1):

| ID | Decision |
|---|---|
| U1 | Service epics, plus business-epic tags |
| U2 | Do not disturb Epic 1 work already implemented |
| U3 | Soft ownership; no names |
| U4 | Full template |
| U5 | New versions in place, plus folders 22 and 23 |
| U6 | No Jira access |
| U7 | Dates tentative and unchanged; finish within 8 months |
| U8 | No human stops; maximum subagents |
| U9 | Use the existing BRDs and the AI-SDLC (HVE Core) agents |
| U10 | Large Excalidraw diagram |

**Executor:** DeepSeek v4.1 Flash in T3 Code (OpenCode provider). OpenCode cannot see the Claude or Copilot agents, so Tasks 3–5 build and prove a compatibility layer first.

---

## 2. File structure

| Path | Responsibility |
|---|---|
| `22 Microservice Realignment/compat/common.py` | Paths, the 19-service table, versioning, header, jsonl, sha256, opencode exe lookup |
| `22 Microservice Realignment/compat/bootstrap.py` | Creates folders 22 and 23, `_work/msr/*` and `status.json` |
| `22 Microservice Realignment/compat/copy_workspace.py` | Builds the AI-SDLC workspace `22/aisdlc/` from folders 18 and 17 (read-only copies) |
| `22 Microservice Realignment/compat/sync_opencode_agents.py` | Generates `.opencode/agent/aisdlc-*.md` and `.opencode/command/aisdlc-*.md` |
| `22 Microservice Realignment/compat/smoke.py` | Proves that the agents load and run, and that there is no MCP or Jira call |
| `22 Microservice Realignment/compat/probe_capacity.py` | Live concurrency ramp; writes `capacity.json` |
| `22 Microservice Realignment/compat/run_parallel.py` | Weighted-budget parallel runner, with retry and quota guard |
| `22 Microservice Realignment/compat/convert_sources.py` | Converts docx, pptx and xlsx to md |
| `22 Microservice Realignment/compat/legacy_index.py` | Parses the 7 story masters into `legacy_index.json` |
| `22 Microservice Realignment/compat/id_scan.py` | Finds the free D-RCV, ADR and DL numbers |
| `22 Microservice Realignment/compat/ownership.py` | Builds the Ownership Map skeleton, then validates it |
| `22 Microservice Realignment/compat/split_plan.py` | Classifier, slices, dependency classes, lanes, Day-1 and depth split, producing `split_plan.json` |
| `22 Microservice Realignment/compat/make_wps.py` | WP files and the queues B, C and D |
| `22 Microservice Realignment/compat/docgen.py` | Template and Rules v1, Change Register v1, Tracker v1, Jira file |
| `22 Microservice Realignment/compat/xlsx_write.py` | Small openpyxl writer (header style, freeze, autofilter) |
| `22 Microservice Realignment/compat/number_registers.py` | Turns CG and ASM candidates into GAP-nnnn and ASM-nnnn; rewrites citations |
| `22 Microservice Realignment/compat/assemble.py` | Stage C masters, catalogue and Day-1 Allocation, plus PRD references |
| `22 Microservice Realignment/compat/build_arch_diagram.py` | Epic diagrams and the master and wave Excalidraw diagrams, with SVG |
| `22 Microservice Realignment/compat/tests/test_*.py` | unittest tests, one file per script |
| `22 Microservice Realignment/checks/run_all.py` | Checks C01–C20 |
| `ROOT/opencode.json`, `ROOT/AGENTS.md` | OpenCode project config and run rules |
| `ROOT/.opencode/agent/` (fallback: `agents/`) | Generated agents |
| `_work/msr/` | Scratch area: `wp/`, `plan/`, `extract/`, `fragments/`, `gaps/`, `assumptions/`, `editlog/`, `logs/`, `smoke/`, `probe/`, `status.json` |
| Outputs | Listed in Appendix R §R8 (folders 02–16, 22, 23) |

**Read-only throughout:**
- Folders `17 …`, `18 …` and `21 …`.
- Every existing file. A new version is always a new file.

**Running the tests.** The test command (it is the same everywhere) is:

```powershell
python -I -m unittest discover -s "22 Microservice Realignment/compat/tests" -t "22 Microservice Realignment/compat" -v
```

---

## 3. Tasks — Stage A (coordinator session, in order, no stops)

### Task 1: Common helpers and bootstrap folders

**Files:**
- Create: `22 Microservice Realignment/compat/common.py`
- Create: `22 Microservice Realignment/compat/bootstrap.py`
- Create: `22 Microservice Realignment/compat/tests/__init__.py` (empty)
- Test: `22 Microservice Realignment/compat/tests/test_common.py`

- [ ] **Step 1: Create the folders the test needs.** Run this command (the folder names contain spaces, so keep the quotes):

```powershell
New-Item -ItemType Directory -Force "22 Microservice Realignment/compat/tests" | Out-Null; New-Item -ItemType File -Force "22 Microservice Realignment/compat/tests/__init__.py" | Out-Null
```

- [ ] **Step 2: Write the failing test** `tests/test_common.py`:

```python
import tempfile, unittest
from pathlib import Path
import common

class TestCommon(unittest.TestCase):
    def test_services(self):
        self.assertEqual(len(common.SERVICES), 19)
        self.assertEqual(common.svc("P3")["service"], "rwb-case")
        self.assertEqual(common.svc("P1")["schema"], "rwb_source_data")
        self.assertEqual(common.svc("P3")["topic"], "rwb.case.events.v1")
        self.assertEqual(common.svc("S6")["queue"], "rwb-debtsale")
        self.assertEqual(common.svc("P3")["base"], "/api/recovery/case/v1")
        self.assertEqual(common.svc("S9")["wave"], 4)

    def test_next_version(self):
        with tempfile.TemporaryDirectory() as d:
            for n in ["Recovery Workbench Release Plan v4.docx", "Recovery Workbench Release Plan v3.docx",
                      "Recovery Workbench Release Plan Extra v9.docx"]:
                (Path(d) / n).write_text("x")
            self.assertEqual(common.next_version(Path(d), "Recovery Workbench Release Plan"), 5)
            self.assertEqual(common.next_version(Path(d), "Recovery Workbench Nothing"), 1)
            self.assertEqual(common.latest_path(Path(d), "Recovery Workbench Release Plan").name,
                             "Recovery Workbench Release Plan v4.docx")

    def test_header_and_jsonl(self):
        h = common.header("22 November 2026")
        self.assertTrue(h.startswith("SCB Collections and Recovery. Henka Group, 22 November 2026."))
        with tempfile.TemporaryDirectory() as d:
            p = Path(d) / "a.jsonl"
            common.append_jsonl(p, {"a": 1}); common.append_jsonl(p, {"a": 2})
            self.assertEqual([r["a"] for r in common.read_jsonl(p)], [1, 2])

if __name__ == "__main__":
    unittest.main()
```

- [ ] **Step 3: Run the test and confirm it fails.** Use the test command from section 2. Expected: `ModuleNotFoundError: No module named 'common'`.

- [ ] **Step 4: Write `compat/common.py`.**

```python
"""Shared paths, constants and helpers for the D-RCV-53 realignment run. Run all scripts as python -I."""
import datetime, hashlib, json, os, re, shutil, threading
from pathlib import Path

COMPAT = Path(__file__).resolve().parent
R22 = COMPAT.parent
ROOT = R22.parent
R23 = ROOT / "23 Document Gaps"
WORK = ROOT / "_work" / "msr"
CHECKS = R22 / "checks"
WS = R22 / "aisdlc"
F17 = ROOT / "17 AI-First SDLC Repository v2"
F18 = ROOT / "18 E2E Recovery Workbench"
STORIES = ROOT / "04 User stories"
SUBDIRS = ["wp", "plan", "extract", "fragments", "gaps", "assumptions", "editlog", "logs", "smoke", "probe"]
MODEL = "opencode-go/deepseek-v4.1-flash"
VARIANT = "max"
TOOL_LINE = "T3 Code / OpenCode / DeepSeek v4.1 Flash"
RUN_DATE = "22 November 2026"
DECISION = "D-RCV-53"

# code, short, display name, wave (Arch v5)
_SVC = [
    ("P1", "source-data", "Source data", 1), ("P2", "integration", "Integration", 1),
    ("P3", "case", "Case and workflow", 1), ("P4", "access", "Access and authority", 1),
    ("P5", "document", "Document", 1), ("P6", "comms", "Communications", 1),
    ("P7", "decision", "Decision and rules", 1), ("P8", "payment", "Payment", 2),
    ("P9", "reporting", "Reporting", 1), ("P10", "agent", "Agent", 1),
    ("S1", "valuation", "Valuation and route", 3), ("S2", "treatment", "Treatment and offer", 2),
    ("S3", "guarantee", "Guarantee", 3), ("S4", "litigation", "Litigation", 3),
    ("S5", "asset", "Asset", 2), ("S6", "debtsale", "Debt sale", 3),
    ("S7", "writeoff", "Write-off", 4), ("S8", "deviation", "Deviation", 2),
    ("S9", "partner", "Partner", 4),
]

def _row(code, short, name, wave):
    return {"code": code, "short": short, "name": name, "wave": wave, "service": f"rwb-{short}",
            "schema": "rwb_" + short.replace("-", "_"), "base": f"/api/recovery/{short}/v1",
            "topic": f"rwb.{short}.events.v1", "queue": f"rwb-{short}", "epic": f"RWB-SVC-{code}",
            "package": "th.co.scb.ace.workbench.recovery." + short.replace("-", "")}

SERVICES = [_row(*s) for s in _SVC]
_BY = {s["code"]: s for s in SERVICES}
PLT_EPICS = ["TPL", "LIB", "WF", "DB", "EVT", "EDGE", "OBS"]
ITG_EPICS = ["W1", "W2", "W3", "W4", "NFR"]
OWNER = {
    "TechX": "TechX (suggested; any team may pick up this story)",
    "ACE": "ACE team (suggested; any team may pick up this story)",
    "INFRA": "SCB IT infrastructure (suggested; any team may pick up this story)",
    "DEVOPS": "DevOps team (suggested; any team may pick up this story)",
    "QA": "QA team (suggested; any team may pick up this story)",
}
WT_OWNER = {"CON": "TechX", "APP": "TechX", "ITG": "TechX", "DB": "ACE", "INF": "INFRA", "OPS": "DEVOPS"}
WT_NAME = {"CON": "Contract", "APP": "App development", "DB": "ACE DB", "INF": "Infrastructure",
           "OPS": "DevOps", "ITG": "Integration"}
WT_SUFFIX = {"CON": " - contract", "APP": "", "DB": " - ACE DB", "INF": " - infrastructure",
             "OPS": " - deployment", "ITG": " - integration"}
ID_RE = re.compile(r"^RWB-(P10|P[1-9]|S[1-9]|PLT|ITG)-(E[1-8]\d{3}|TE\d{3}|AD\d{3}|DM\d{3}|ACE\d{3}|NF\d{2}|N\d{3}|W[1-4]J\d{2})-(CON|APP|DB|INF|OPS|ITG)(-[2-9])?$")
LEGACY_RE = re.compile(r"RWB-(E[1-8]|TE|AD|DM|ACE)-(\d{3})")

def svc(code):
    return _BY[code]

def leg_compact(key):
    """RWB-E1-018 -> E1018 ; NF-06 -> NF06"""
    m = LEGACY_RE.fullmatch(key)
    if m:
        return m.group(1) + m.group(2)
    return key.replace("RWB-", "").replace("-", "")

def story_id(scope, legacy_key, wt, n=None):
    sid = f"RWB-{scope}-{leg_compact(legacy_key)}-{wt}" + (f"-{n}" if n else "")
    assert ID_RE.match(sid), sid
    return sid

def _vre(stem):
    return re.compile(r"^" + re.escape(stem) + r" v(\d+)(\.[A-Za-z0-9]+)?$")

def versions(folder, stem):
    folder = Path(folder)
    if not folder.exists():
        return []
    out = []
    for p in folder.iterdir():
        m = _vre(stem).match(p.name)
        if m:
            out.append((int(m.group(1)), p))
    return sorted(out, key=lambda t: (t[0], t[1].is_dir(), t[1].name))

def next_version(folder, stem):
    v = versions(folder, stem)
    return (max(n for n, _ in v) + 1) if v else 1

def latest_path(folder, stem, ext=None):
    v = [(n, p) for n, p in versions(folder, stem) if ext is None or p.suffix.lower() == ext.lower()
         or (ext == "dir" and p.is_dir())]
    return v[-1][1] if v else None

def header(date=RUN_DATE):
    return f"SCB Collections and Recovery. Henka Group, {date}.\n(C) Siam Commercial Bank and Henka Pte Ltd\n"

_lock = threading.Lock()

def append_jsonl(path, obj):
    path = Path(path); path.parent.mkdir(parents=True, exist_ok=True)
    with _lock, open(path, "a", encoding="utf-8") as f:
        f.write(json.dumps(obj, ensure_ascii=False) + "\n")

def read_jsonl(path):
    path = Path(path)
    if not path.exists():
        return []
    return [json.loads(l) for l in path.read_text(encoding="utf-8").splitlines() if l.strip()]

def read_json(path, default=None):
    path = Path(path)
    return json.loads(path.read_text(encoding="utf-8")) if path.exists() else default

def write_json(path, obj):
    path = Path(path); path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_suffix(path.suffix + ".tmp")
    tmp.write_text(json.dumps(obj, ensure_ascii=False, indent=2), encoding="utf-8")
    os.replace(tmp, path)

def sha256(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for b in iter(lambda: f.read(1 << 20), b""):
            h.update(b)
    return h.hexdigest()

def opencode_exe():
    w = shutil.which("opencode")
    if w:
        exe = Path(w).parent / "node_modules" / "@opencode" / "cli" / "bin" / "opencode.exe"
        if exe.exists():
            return str(exe)
        return w
    raise SystemExit("opencode not found on PATH")

def runtime():
    """Model string chosen by smoke.py (with or without the #max variant)."""
    rt = read_json(WORK / "plan" / "runtime.json", {})
    return rt.get("model", f"{MODEL}#{VARIANT}")

def today():
    return datetime.date.today().strftime("%d %B %Y").lstrip("0")

# ---- candidate gaps / assumptions (numbered only in step D1 by number_registers.py) ----
_ctr = {}

def reset_cands(wp):
    for k in ("gaps", "assumptions"):
        p = WORK / k / f"{wp}.jsonl"
        if p.exists():
            p.unlink()
    _ctr.pop((wp, "g"), None); _ctr.pop((wp, "a"), None)

def _next(wp, kind):
    with _lock:
        _ctr[(wp, kind)] = _ctr.get((wp, kind), 0) + 1
        return _ctr[(wp, kind)]

def add_gap(wp, title, description, gtype="Missing", severity="P2", source="", section="", area="",
            owner_role="Tech lead", legacy_ref="", asm="", proposed="", needed_by_wave="", evidence=""):
    gid = f"CG-{wp}-{_next(wp, 'g')}"
    append_jsonl(WORK / "gaps" / f"{wp}.jsonl", {"id": gid, "title": title, "source": source, "section": section,
                 "description": description, "evidence": evidence, "type": gtype, "area": area, "severity": severity,
                 "needed_by_wave": needed_by_wave, "legacy_ref": legacy_ref, "owner_role": owner_role,
                 "asm": asm, "proposed": proposed, "wp": wp})
    return gid

def add_asm(wp, text, why, read="", gap="", applied_in="", confidence="Medium", confirm="", impact=""):
    aid = f"ASM-{wp}-{_next(wp, 'a')}"
    append_jsonl(WORK / "assumptions" / f"{wp}.jsonl", {"id": aid, "text": text, "why": why, "read": read,
                 "gap": gap, "applied_in": applied_in, "confidence": confidence, "confirm": confirm,
                 "impact": impact, "wp": wp})
    return aid
```

- [ ] **Step 5: Write `compat/bootstrap.py`.**

```python
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
from common import ROOT, R22, R23, WORK, CHECKS, SUBDIRS, write_json, sha256

TOP_SKIP = {"_work", "22 Microservice Realignment", "23 Document Gaps", ".opencode", ".git"}
ANY_SKIP = {".git", "node_modules", "target", "build", "dist", ".gradle", "rwb-wt", "temp"}

def baseline():
    """sha256 of every file that exists before the run. Check C01 proves none of them changed."""
    out = {}
    for p in ROOT.rglob("*"):
        rel = p.relative_to(ROOT)
        if rel.parts[0] in TOP_SKIP or ANY_SKIP & set(rel.parts) or not p.is_file():
            continue
        try:
            out[rel.as_posix()] = sha256(p)
        except OSError:
            pass
    write_json(WORK / "plan" / "baseline.json", out)
    return len(out)

def main():
    for d in [R22, R23, CHECKS, CHECKS / "reports", R22 / "compat" / "tests"] + [WORK / s for s in SUBDIRS]:
        d.mkdir(parents=True, exist_ok=True)
    if not (WORK / "status.json").exists():
        write_json(WORK / "status.json", {})
    n = baseline() if not (WORK / "plan" / "baseline.json").exists() else "kept"
    print("BOOTSTRAP OK", WORK, "baseline files:", n)

if __name__ == "__main__":
    main()
```

- [ ] **Step 6: Run the tests and bootstrap.** Run the test command, then:

```powershell
python -I "22 Microservice Realignment/compat/bootstrap.py"
```

Expected: 3 tests `OK`, then `BOOTSTRAP OK …\_work\msr baseline files: <n>`. The baseline is taken once, before any agent runs, and is never rewritten.

- [ ] **Step 7: Confirm the plan copy.** `2026-11-22-recovery-microservice-realignment-implementation-plan.md` must exist at ROOT. If it is missing, copy this plan file there. (No commit.)

---

### Task 2: OpenCode project config and root run rules (K6, K7)

**Files:**
- Create: `ROOT/opencode.json`
- Create: `ROOT/AGENTS.md`

- [ ] **Step 1: Write `opencode.json`.**

```json
{
  "$schema": "https://opencode.ai/config.json",
  "model": "opencode-go/deepseek-v4.1-flash",
  "mcp": { "jira": { "enabled": false } },
  "permission": { "webfetch": "deny", "edit": "allow", "bash": "allow" }
}
```

- [ ] **Step 2: Verify the merged config.**

```powershell
opencode debug config
```

Expected: the JSON shows `"jira"` with `"enabled": false` and `"webfetch": "deny"`, and there is no validation error. Two fallbacks:
- **Validation error on the `mcp` entry:** replace it with `"mcp": {}`. Then add `"tools": {"jira_*": false}` and record the assumption `ASM-A2-1` "jira MCP disabled through the tools map".
- **Another MCP server listed with `enabled: true`** (atlassian, gitlab or playwright): add `"<name>": {"enabled": false}` for it and run the command again.

How to write an assumption is shown in Task 15, step 1. Use the file `_work/msr/assumptions/A2.jsonl`.

- [ ] **Step 3: Write `ROOT/AGENTS.md`.**

```markdown
# Realignment run rules (D-RCV-53). Read before any work in this folder.

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
```

- [ ] **Step 4: Check that OpenCode reads it.**

```powershell
opencode run --model opencode-go/deepseek-v4.1-flash "Quote rule 14 of AGENTS.md word for word and nothing else."
```

Expected: the output starts with "Parallel work: when your WP says". If it does not, add `"instructions": ["AGENTS.md"]` to `opencode.json` and run the command again.

---

### Task 3: AI-SDLC workspace copy (K4)

**Files:**
- Create: `22 Microservice Realignment/compat/copy_workspace.py`
- Test: `22 Microservice Realignment/compat/tests/test_copy_workspace.py`

- [ ] **Step 1: Write the failing test.**

```python
import tempfile, unittest
from pathlib import Path
import copy_workspace as cw

class TestCopy(unittest.TestCase):
    def test_copy_latest(self):
        with tempfile.TemporaryDirectory() as d:
            d = Path(d)
            (d / "src/.github/agents").mkdir(parents=True)
            (d / "src/.github/agents/planner.agent.md").write_text("a")
            (d / "prds").mkdir()
            for n in ["p3-case-fsd-v3.md", "p3-case-fsd-v4.md", "nfr.md"]:
                (d / "prds" / n).write_text(n)
            cw.copy_tree(d / "src/.github", d / "ws/.github")
            cw.copy_latest_md(d / "prds", d / "ws/docs/prds")
            self.assertTrue((d / "ws/.github/agents/planner.agent.md").exists())
            names = sorted(p.name for p in (d / "ws/docs/prds").iterdir())
            self.assertEqual(names, ["nfr.md", "p3-case-fsd-v4.md"])
```

- [ ] **Step 2: Run the test.** Expected: FAIL, `No module named 'copy_workspace'`.

- [ ] **Step 3: Write `copy_workspace.py`.**

```python
import re, shutil, sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
from common import WS, F17, F18

def copy_tree(src, dst):
    shutil.copytree(src, dst, dirs_exist_ok=True)

def copy_latest_md(src, dst):
    """Copy *.md, keeping only the highest -vN of each family."""
    dst.mkdir(parents=True, exist_ok=True)
    best = {}
    for p in Path(src).glob("*.md"):
        m = re.match(r"^(.*?)-v(\d+)\.md$", p.name)
        fam, v = (m.group(1), int(m.group(2))) if m else (p.stem, 0)
        if fam not in best or v > best[fam][0]:
            best[fam] = (v, p)
    for _, p in best.values():
        shutil.copy2(p, dst / p.name)

def main():
    copy_tree(F18 / "aisdlc" / ".github", WS / ".github")
    copy_tree(F17 / "requirement" / "legacy", WS / "requirement" / "legacy")
    copy_latest_md(F17 / "docs" / "brds", WS / "docs" / "brds")
    copy_latest_md(F17 / "docs" / "prds", WS / "docs" / "prds")
    (WS / ".claude-commands").mkdir(parents=True, exist_ok=True)
    for n in ["brd-builder.md", "prd-builder.md", "backlog-builder.md"]:
        shutil.copy2(F18 / ".claude" / "commands" / n, WS / ".claude-commands" / n)
    for d in ["docs/increments", "output", "requirement/legacy/_converted"]:
        (WS / d).mkdir(parents=True, exist_ok=True)
    tm = WS / "requirement" / "Traceability_Matrix.md"
    if not tm.exists():
        tm.write_text("# Traceability Matrix (realignment workspace)\n\n| Source | ID | Target |\n|---|---|---|\n", encoding="utf-8")
    print("WORKSPACE OK", WS)

if __name__ == "__main__":
    main()
```

- [ ] **Step 4: Run the tests, then the script.**

```powershell
python -I "22 Microservice Realignment/compat/copy_workspace.py"
```

Expected: tests OK, then `WORKSPACE OK`. These three folders must now be non-empty:
- `22 Microservice Realignment/aisdlc/.github/agents`
- `22 Microservice Realignment/aisdlc/docs/brds`
- `22 Microservice Realignment/aisdlc/.claude-commands`

---

### Task 4: OpenCode agent generator (K1, K2, K3, K5)

**Files:**
- Create: `22 Microservice Realignment/compat/sync_opencode_agents.py`
- Test: `22 Microservice Realignment/compat/tests/test_sync_agents.py`

- [ ] **Step 1: Write the failing test.**

```python
import tempfile, unittest
from pathlib import Path
import yaml
import sync_opencode_agents as s

AGENT = '''---
description: "Use when: writing a spec"
name: "Technical Specifier"
tools: [read, edit, search, execute, agent]
agents: ["Compliance Reviewer"]
---
You run in the Claude Code runtime.
Use TodoWrite for tasks and the Agent tool to spawn reviewers.
'''
REV = '''---
description: "Use when: reviewing"
name: "Compliance Reviewer"
tools: [read]
---
Review it.
'''
CMD = '''---
description: AISDLC agent - BRD Builder
---
Convert .docx/.pptx with `textutil -convert txt` and continue.
Input: $ARGUMENTS
'''

class TestSync(unittest.TestCase):
    def test_generate(self):
        with tempfile.TemporaryDirectory() as d:
            d = Path(d)
            (d / "agents").mkdir(); (d / "cmds").mkdir()
            (d / "agents/specify.agent.md").write_text(AGENT, encoding="utf-8")
            (d / "agents/reviewer.agent.md").write_text(REV, encoding="utf-8")
            (d / "agents/agent-frontmatter-reference.md").write_text("ignore", encoding="utf-8")
            (d / "cmds/brd-builder.md").write_text(CMD, encoding="utf-8")
            out = s.generate(d / "agents", d / "cmds", d / "root", "agent")
            names = sorted(p.name for p in (d / "root/.opencode/agent").iterdir())
            self.assertEqual(names, ["aisdlc-brd-builder.md", "aisdlc-msr-worker.md",
                                     "aisdlc-reviewer.md", "aisdlc-specify.md"])
            txt = (d / "root/.opencode/agent/aisdlc-specify.md").read_text(encoding="utf-8")
            fm = yaml.safe_load(txt.split("---")[1])
            self.assertEqual(fm["mode"], "all")
            self.assertFalse(fm["tools"]["webfetch"])
            self.assertNotIn("Claude Code runtime", txt)
            self.assertIn("todowrite", txt)
            self.assertIn("aisdlc-reviewer", txt)
            self.assertIn("No human approval is required", txt)
            brd = (d / "root/.opencode/agent/aisdlc-brd-builder.md").read_text(encoding="utf-8")
            self.assertNotIn("textutil", brd)
            self.assertIn("convert_sources.py", brd)
            self.assertTrue((d / "root/.opencode/command/aisdlc-brd-builder.md").exists())
            self.assertIn("$ARGUMENTS", (d / "root/.opencode/command/aisdlc-brd-builder.md").read_text(encoding="utf-8"))
            self.assertEqual(len(out), 4)
```

- [ ] **Step 2: Run the test.** Expected: FAIL, `No module named 'sync_opencode_agents'`.

- [ ] **Step 3: Write `sync_opencode_agents.py`.**

```python
"""Generate OpenCode agents/commands from the AI-SDLC (HVE Core) agent sources. Never edits folder 18."""
import argparse, re, sys
from pathlib import Path
import yaml
sys.path.insert(0, str(Path(__file__).resolve().parent))
from common import ROOT, WS, MODEL, COMPAT

TOOLS = {"read": True, "grep": True, "glob": True, "list": True, "edit": True, "write": True,
         "bash": True, "task": True, "todowrite": True, "todoread": True, "webfetch": False}
HEADER = ("You are the `{name}` OpenCode agent (model DeepSeek v4.1 Flash, run from T3 Code). "
          "Delegate only through the `task` tool, and only to: {subs}. Use `todowrite` for task lists. "
          "The AI-SDLC workspace root is `22 Microservice Realignment/aisdlc/`; every relative path in "
          "this prompt (.github/contexts, .github/rules, docs/brds, docs/prds, requirement/legacy, "
          "output/<RUN_ID>) resolves there.")
OVERLAY = """## Realignment overlay (D-RCV-53) — overrides anything above
- This run is the D-RCV-53 realignment. No human approval is required to proceed.
- Treat any missing approval or status (for example "BRD status must be Approved") as an assumption:
  append {"id":"ASM-<WP>-<n>","text":...,"why":...,"read":...,"confidence":"Medium"} to
  _work/msr/assumptions/<WP>.jsonl and continue with status Draft.
- Never ask the user a question. Never call Jira, Confluence, GitLab, Figma or the web.
- Never start a later lifecycle stage on your own. Stop only for a safety, credential or production-data issue.
- Convert .docx/.pptx/.xlsx only with: python -I "22 Microservice Realignment/compat/convert_sources.py" <file> <outdir>
- Follow ROOT AGENTS.md rules 1-14. Edit log tool line: T3 Code / OpenCode / DeepSeek v4.1 Flash."""
WORKER_BODY = """You are the realignment worker. Follow the WP file you are given exactly, top to bottom.
Read every file under "Read only" before writing. Write only the files under "Write only".
Use the template, split rules, DP table, dependency classes and Day-1 rule in
"22 Microservice Realignment/Recovery Workbench Microservice Story Template and Rules v1.md".
When the WP says "fanout: F", give each legacy story to its own task subagent (aisdlc-msr-worker),
up to F in parallel in a single message, each with the WP path and its one legacy key; then merge nothing —
each subagent writes its own files. Finish with the quick check in AGENTS.md rule 12."""
FIXES = [
    (re.compile(r"(?im)^.*claude code runtime.*$\n?"), ""),
    (re.compile(r"\bTodoWrite\b"), "todowrite"),
    (re.compile(r"\bthe Agent tool\b"), "the task tool"),
    (re.compile(r"\bAgent tool\b"), "task tool"),
    (re.compile(r"`?textutil -convert txt`?"), '`python -I "22 Microservice Realignment/compat/convert_sources.py" <file> requirement/legacy/_converted`'),
    (re.compile(r"(?i)human-started stage[^.\n]*\.?"), "Started by the realignment coordinator."),
]

def split_fm(text):
    m = re.match(r"^---\r?\n(.*?)\r?\n---\r?\n?(.*)$", text, re.S)
    if not m:
        return {}, text
    return (yaml.safe_load(m.group(1)) or {}), m.group(2)

def fix(body):
    for rx, rep in FIXES:
        body = rx.sub(rep, body)
    return body

def render(name, desc, body, subs):
    fm = {"description": str(desc or name)[:900], "mode": "all", "model": MODEL, "temperature": 0.1, "tools": TOOLS}
    head = HEADER.format(name=name, subs=", ".join(subs) if subs else "aisdlc-msr-worker")
    return "---\n" + yaml.safe_dump(fm, sort_keys=False, allow_unicode=True) + "---\n" + head + "\n\n" + fix(body).strip() + "\n\n" + OVERLAY + "\n"

def generate(src_agents, src_cmds, out_root, layout="agent"):
    adir = Path(out_root) / ".opencode" / layout
    cdir = Path(out_root) / ".opencode" / ("command" if layout == "agent" else "commands")
    adir.mkdir(parents=True, exist_ok=True); cdir.mkdir(parents=True, exist_ok=True)
    srcs = sorted(p for p in Path(src_agents).glob("*.agent.md"))
    parsed = {p: split_fm(p.read_text(encoding="utf-8")) for p in srcs}
    by_display = {str(fm.get("name", "")): "aisdlc-" + p.name[:-len(".agent.md")] for p, (fm, _) in parsed.items()}
    written = []
    for p, (fm, body) in parsed.items():
        name = "aisdlc-" + p.name[:-len(".agent.md")]
        subs = [by_display.get(a, "aisdlc-" + re.sub(r"[^a-z0-9]+", "-", a.lower()).strip("-")) for a in (fm.get("agents") or [])]
        (adir / f"{name}.md").write_text(render(name, fm.get("description"), body, subs), encoding="utf-8")
        written.append(name)
    for p in sorted(Path(src_cmds).glob("*.md")):
        fm, body = split_fm(p.read_text(encoding="utf-8"))
        name = "aisdlc-" + p.stem
        (adir / f"{name}.md").write_text(render(name, fm.get("description"), body, []), encoding="utf-8")
        cmd_fm = yaml.safe_dump({"description": str(fm.get("description", name)), "agent": name}, sort_keys=False)
        (cdir / f"{name}.md").write_text("---\n" + cmd_fm + "---\n" + fix(body).strip() + "\n", encoding="utf-8")
        written.append(name)
    (adir / "aisdlc-msr-worker.md").write_text(
        render("aisdlc-msr-worker", "Realignment worker: executes one WP file exactly.", WORKER_BODY, []), encoding="utf-8")
    written.append("aisdlc-msr-worker")
    return written

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--layout", choices=["agent", "agents"], default="agent")
    a = ap.parse_args()
    names = generate(WS / ".github" / "agents", WS / ".claude-commands", ROOT, a.layout)
    print(f"GENERATED {len(names)} agents into .opencode/{a.layout}: " + ", ".join(sorted(names)))

if __name__ == "__main__":
    main()
```

- [ ] **Step 4: Run the tests, then generate.**

```powershell
python -I "22 Microservice Realignment/compat/sync_opencode_agents.py"
```

Expected: tests OK, then `GENERATED 17 agents into .opencode/agent: aisdlc-api-tester, …, aisdlc-msr-worker, …`. The 17 are the 13 sources, the 3 commands and the worker. Expected source names:
- api-tester
- context-builder
- context-updater
- figma-extractor
- functional-automation-test
- implement
- planner
- qa-test-case-generator
- reviewer
- specify
- technical-documenter
- traceability-manager

If fewer files exist, the count is lower: record the actual count as an assumption and continue.

---

### Task 5: Smoke test for the compatibility layer (3.3)

**Files:**
- Create: `22 Microservice Realignment/compat/smoke.py`
- Output: `_work/msr/smoke/result.json`, `_work/msr/plan/runtime.json`

- [ ] **Step 1: Write `smoke.py`.**

```python
"""Prove generated agents load and run under OpenCode with DeepSeek. Retries and falls back; never stops."""
import json, re, subprocess, sys, time
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
from common import ROOT, WORK, MODEL, VARIANT, opencode_exe, write_json, append_jsonl

EXE = opencode_exe()

def oc(args, timeout=900):
    p = subprocess.run([EXE] + args, cwd=ROOT, capture_output=True, text=True, encoding="utf-8",
                       errors="replace", timeout=timeout)
    return p.returncode, p.stdout, p.stderr

def agent_ids():
    rc, out, err = oc(["debug", "agents"], 120)
    i = out.find("[")
    try:
        return {a["id"] for a in json.loads(out[i:])}
    except Exception:
        return set()

def asm(text, why):
    append_jsonl(WORK / "assumptions" / "A5.jsonl", {"id": f"ASM-A5-{int(time.time()*1000)%100000}",
                 "text": text, "why": why, "read": "opencode debug agents / opencode run", "confidence": "High"})

def main():
    res = {"layout": None, "model": None, "worker": False, "brd": False, "mcp_calls": None}
    ids = agent_ids()
    if "aisdlc-msr-worker" in ids:
        res["layout"] = "agent"
    else:
        subprocess.run([sys.executable, "-I", str(Path(__file__).parent / "sync_opencode_agents.py"), "--layout", "agents"], check=False)
        ids = agent_ids()
        res["layout"] = "agents" if "aisdlc-msr-worker" in ids else "none"
        asm(f"OpenCode agent folder is .opencode/{res['layout']}", "singular folder not loaded")
    res["agents_loaded"] = sorted(i for i in ids if i.startswith("aisdlc-"))
    target = WORK / "smoke" / "worker.txt"
    for model in [f"{MODEL}#{VARIANT}", MODEL]:
        for attempt in range(3):
            if target.exists():
                target.unlink()
            agent_args = ["--agent", "aisdlc-msr-worker"] if res["layout"] != "none" else []
            rc, out, err = oc(["run", "--auto", "--model", model] + agent_args +
                              ["Write the text OK to the file _work/msr/smoke/worker.txt and nothing else."])
            if target.exists() and "OK" in target.read_text(encoding="utf-8", errors="replace"):
                res["worker"], res["model"] = True, model
                break
            time.sleep(10 * (attempt + 1))
        if res["worker"]:
            break
    if res["model"] != f"{MODEL}#{VARIANT}":
        asm(f"Model string used: {res['model'] or MODEL}", "variant #max rejected or worker failed")
    model = res["model"] or MODEL
    write_json(WORK / "plan" / "runtime.json", {"model": model, "layout": res["layout"]})
    brief = WORK / "smoke" / "brd-brief.md"
    brief.write_text("BRD name: Smoke_Test\nFocus: one paragraph only about recovery case ownership.\n"
                     "Write to 22 Microservice Realignment/aisdlc/docs/brds/_smoke/Smoke_Test.md\n"
                     "Sections 1 and 2 only. Status Draft.\nThis is a smoke test of the agent.\n", encoding="utf-8")
    out_md = ROOT / "22 Microservice Realignment" / "aisdlc" / "docs" / "brds" / "_smoke" / "Smoke_Test.md"
    for attempt in range(3):
        oc(["run", "--auto", "--model", model, "--agent", "aisdlc-brd-builder", "--file", str(brief),
            "Follow the attached brief exactly."])
        if out_md.exists() and out_md.read_text(encoding="utf-8", errors="replace").lstrip().startswith("---"):
            res["brd"] = True
            break
    logdir = Path.home() / ".local" / "share" / "opencode" / "log"
    latest = max(logdir.glob("*.log"), key=lambda p: p.stat().st_mtime, default=None)
    txt = latest.read_text(encoding="utf-8", errors="replace")[-400000:] if latest else ""
    res["mcp_calls"] = len(re.findall(r"(?i)mcp.*(jira|atlassian|gitlab)", txt))
    write_json(WORK / "smoke" / "result.json", res)
    print("SMOKE", json.dumps(res))

if __name__ == "__main__":
    main()
```

- [ ] **Step 2: Run the smoke test.**

```powershell
python -I "22 Microservice Realignment/compat/smoke.py"
```

Expected: a line `SMOKE {"layout": "agent", "model": "opencode-go/deepseek-v4.1-flash#max", "worker": true, "brd": true, "mcp_calls": 0, …}`. What to do if a value is wrong:

| Result | Action |
|---|---|
| `"worker": false` | Run `opencode run --model opencode-go/deepseek-v4.1-flash "say OK"`. If that works but the worker does not, the agent frontmatter is wrong. Delete the `tools:` block in the generator (`TOOLS` → `{}`), regenerate, and rerun the smoke test. Record an ASM. |
| `"brd": false` after 3 tries | Continue anyway. Stage B BRD WPs then run the brd-builder **body** as plain text, attached with `--file` to `aisdlc-msr-worker`. Set `"brd_fallback": true` in `runtime.json` by hand, and record an ASM. |
| `"mcp_calls"` above 0 | Recheck Task 2, step 2. |

---

### Task 6: Live concurrency probe for DeepSeek v4.1 Flash

**Files:**
- Create: `22 Microservice Realignment/compat/probe_capacity.py`
- Output: `_work/msr/plan/capacity.json`

The probe runs two parts:
- **Part 1, processes.** It launches parallel `opencode run` processes at 4, 8, 12, 16, 20, 24, 28 and 32. The ramp stops at the first level where any process fails, or where the median latency is more than 3 times the 4-process baseline.
- **Part 2, in-session subagents.** One session is asked to launch 12, then 20, task subagents in a single message. Their real overlap is read back from `opencode.db`, read-only.

Each probe prompt is tiny, so the cost to quota is small.

- [ ] **Step 1: Write `probe_capacity.py`.**

```python
import json, sqlite3, statistics, subprocess, sys, time
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
from common import ROOT, WORK, opencode_exe, runtime, write_json

EXE = opencode_exe()
LEVELS = [4, 8, 12, 16, 20, 24, 28, 32]

def one(i, model):
    t = time.time()
    try:
        p = subprocess.run([EXE, "run", "--model", model, "--title", f"msr-probe-{i}", "Reply with exactly: OK"],
                           cwd=ROOT, capture_output=True, text=True, encoding="utf-8", errors="replace", timeout=600)
        ok = p.returncode == 0 and "OK" in p.stdout
        err = (p.stderr or "")[-300:]
    except subprocess.TimeoutExpired:
        ok, err = False, "timeout"
    return {"ok": ok, "secs": round(time.time() - t, 1), "err": err}

def ramp(model):
    results, baseline, best = {}, None, 0
    for n in LEVELS:
        with ThreadPoolExecutor(max_workers=n) as ex:
            r = list(ex.map(lambda i: one(i, model), range(n)))
        med = statistics.median(x["secs"] for x in r)
        fails = [x for x in r if not x["ok"]]
        results[n] = {"median_s": med, "fails": len(fails), "errors": [f["err"] for f in fails][:3]}
        baseline = baseline or med
        if fails or med > 3 * baseline:
            break
        best = n
        time.sleep(20)
    return best, results

def db_overlap(since):
    p = (Path.home() / ".local/share/opencode/opencode.db").as_posix()
    c = sqlite3.connect(f"file:{p}?mode=ro", uri=True)
    rows = c.execute("select id,parent_id,time_created,time_updated from session_v2 where parent_id is not null and time_created>=?",
                     (int(since * 1000),)).fetchall()
    by = {}
    for _id, par, tc, tu in rows:
        by.setdefault(par, []).append((tc, tu))
    best = 0
    for spans in by.values():
        ev = sorted([(a, 1) for a, _ in spans] + [(b, -1) for _, b in spans])
        cur = 0
        for _, d in ev:
            cur += d; best = max(best, cur)
    return best

def fanout(model, k):
    since = time.time()
    prompt = (f"Use the task tool to launch exactly {k} subagents of type general IN ONE MESSAGE (parallel). "
              f"Subagent i must reply 'done i'. Do nothing else. Then reply ALL DONE.")
    subprocess.run([EXE, "run", "--auto", "--model", model, "--title", f"msr-fanout-{k}", prompt],
                   cwd=ROOT, capture_output=True, text=True, encoding="utf-8", errors="replace", timeout=1800)
    time.sleep(5)
    try:
        return db_overlap(since)
    except Exception as e:
        return -1

def main():
    model = runtime()
    best, results = ramp(model)
    fan = {k: fanout(model, k) for k in (12, 20)}
    sess = max([v for v in fan.values() if v > 0] or [10])
    cap = {
        "measured_at": time.strftime("%Y-%m-%d %H:%M"),
        "model": model,
        "process_levels": results,
        "process_max": best or 4,
        "session_subagent_max": sess,
        "budget": best if best else 19,   # largest level that passed; history (19) only if the ramp failed at 4
        "fanout": min(5, sess),
        "historical": {"per_session_max": 10, "global_max": 19, "rate_limit_lines": 0},
    }
    write_json(WORK / "plan" / "capacity.json", cap)
    print("CAPACITY", json.dumps({k: cap[k] for k in ("process_max", "session_subagent_max", "budget", "fanout")}))

if __name__ == "__main__":
    main()
```

- [ ] **Step 2: Run the probe in the background.** Do not wait for it; Task 7 can be built while it runs.

```powershell
python -I "22 Microservice Realignment/compat/probe_capacity.py" *> "_work/msr/probe/probe.log"
```

Expected at the end: `CAPACITY {"process_max": <n>, "session_subagent_max": <m>, "budget": <b>, "fanout": <f>}`. The historical figures predict `budget ≥ 19`, `fanout = 5`.

**Rule:** the run always uses the measured `budget`. It never uses a smaller value, unless `run_parallel.py` lowers it at run time after a 429.

If the probe crashes:
- write `{"budget": 19, "fanout": 5, "process_max": 16, "session_subagent_max": 10}` to `capacity.json` by hand;
- record an ASM ("capacity from history, probe failed");
- continue.

---

### Task 7: Parallel runner with weighted budget, retry and quota guard (K10)

**Files:**
- Create: `22 Microservice Realignment/compat/run_parallel.py`
- Test: `22 Microservice Realignment/compat/tests/test_run_parallel.py`

**Queue format.** `_work/msr/wp/queue-<S>.json` is a list of entries like this:

```json
{"wp": "B-P3-01", "agent": "aisdlc-msr-worker", "file": "_work/msr/wp/B-P3-01.md", "fanout": true, "expect": ["_work/msr/editlog/B-P3-01.md"]}
```

- [ ] **Step 1: Write the failing test.**

```python
import json, tempfile, threading, time, unittest
from pathlib import Path
import run_parallel as rp

class TestBudget(unittest.TestCase):
    def test_weights_never_exceed_cap(self):
        b = rp.Budget(6); peak = [0]; lock = threading.Lock()
        def job(w):
            b.acquire(w)
            with lock:
                peak[0] = max(peak[0], b.used)
            time.sleep(0.05); b.release(w)
        ts = [threading.Thread(target=job, args=(w,)) for w in [6, 1, 1, 3, 2, 6, 1]]
        [t.start() for t in ts]; [t.join() for t in ts]
        self.assertLessEqual(peak[0], 6); self.assertEqual(b.used, 0)

    def test_lower_and_raise(self):
        b = rp.Budget(10); b.lower(); self.assertEqual(b.cap, 8)
        for _ in range(10): b.lower()
        self.assertEqual(b.cap, 4)
        b.last_err -= 700; b.maybe_raise(); self.assertEqual(b.cap, 5)

class TestGuard(unittest.TestCase):
    def test_guard(self):
        with tempfile.TemporaryDirectory() as d:
            p = Path(d) / "c.json"
            now = time.strftime("%Y-%m-%dT%H:%M:%S.000Z", time.gmtime())
            p.write_text(json.dumps({"usageLimits": {"checkedAt": now, "windows": [
                {"kind": "session", "usedPercent": 95, "resetsAt": "2099-01-01T00:00:00.000Z"}]}}))
            self.assertEqual(rp.quota_state(p)[0], "wait")
            p.write_text(json.dumps({"usageLimits": {"checkedAt": now, "windows": [
                {"kind": "weekly", "usedPercent": 97, "resetsAt": "2099-01-01T00:00:00.000Z"}]}}))
            self.assertEqual(rp.quota_state(p)[0], "stop")
            self.assertEqual(rp.quota_state(Path(d) / "missing.json")[0], "ok")

class TestRun(unittest.TestCase):
    def test_retry_then_done(self):
        with tempfile.TemporaryDirectory() as d:
            d = Path(d); calls = {}
            def runner(item, fan):
                calls[item["wp"]] = calls.get(item["wp"], 0) + 1
                if item["wp"] == "W2" and calls["W2"] == 1:
                    return 1, "HTTP 429 Too Many Requests"
                for e in item["expect"]:
                    (d / e).write_text("ok")
                return 0, "done"
            items = [{"wp": f"W{i}", "agent": "a", "file": "x", "fanout": i % 2 == 0, "expect": [f"o{i}.txt"]} for i in range(6)]
            st = rp.run_queue(items, cap=4, fanout=3, runner=runner, base=d, status_path=d / "s.json",
                              backoff=[0, 0, 0], guard=lambda: ("ok", 0))
            self.assertTrue(all(v["state"] == "DONE" for v in st.values()), st)
            self.assertEqual(calls["W2"], 2)
```

- [ ] **Step 2: Run the test.** Expected: FAIL, `No module named 'run_parallel'`.

- [ ] **Step 3: Write `run_parallel.py`.**

```python
"""Keep the measured maximum number of DeepSeek sessions busy. Weighted budget, retry, quota guard."""
import argparse, datetime, json, re, subprocess, sys, threading, time
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
from common import ROOT, WORK, opencode_exe, runtime, read_json, write_json

RATE = re.compile(r"(?i)\b429\b|rate.?limit|too many requests|overloaded|\b5\d\d\b|quota|ECONNRESET|timed? ?out")
T3_CACHE = Path.home() / ".t3" / "caches" / "opencode.json"

class Budget:
    def __init__(self, cap, floor=4):
        self.cap = self.max = cap; self.floor = min(floor, cap); self.used = 0
        self.cv = threading.Condition(); self.last_err = time.time()
    def acquire(self, w):
        with self.cv:
            while self.used > 0 and self.used + w > self.cap:
                self.cv.wait(2)
            self.used += w
    def release(self, w):
        with self.cv:
            self.used -= w; self.cv.notify_all()
    def lower(self):
        with self.cv:
            self.cap = max(self.floor, self.cap - 2); self.last_err = time.time()
    def maybe_raise(self):
        with self.cv:
            if time.time() - self.last_err > 600 and self.cap < self.max:
                self.cap += 1; self.last_err = time.time(); self.cv.notify_all()

def _ts(s):
    return datetime.datetime.strptime(s[:19], "%Y-%m-%dT%H:%M:%S").replace(tzinfo=datetime.timezone.utc).timestamp()

def quota_state(path=T3_CACHE):
    """('ok',0) | ('wait', seconds) | ('stop', resetsAt). Advisory: ignored when the cache is missing or >2 h old."""
    d = read_json(path, None)
    if not d or "usageLimits" not in d:
        return ("ok", 0)
    ul = d["usageLimits"]
    try:
        if time.time() - _ts(ul.get("checkedAt", "1970-01-01T00:00:00")) > 7200:
            return ("ok", 0)
    except Exception:
        return ("ok", 0)
    for w in ul.get("windows", []):
        if w.get("usedPercent", 0) >= 90:
            if w.get("kind") == "session":
                return ("wait", max(60, _ts(w["resetsAt"]) - time.time()))
            if w.get("usedPercent", 0) >= 95:
                return ("stop", w.get("resetsAt"))
    return ("ok", 0)

def oc_runner(item, fanout):
    msg = f"Execute WP {item['wp']}: follow the attached WP file exactly. fanout: {fanout if item.get('fanout') else 0}"
    cmd = [opencode_exe(), "run", "--auto", "--model", runtime(), "--agent", item["agent"],
           "--title", item["wp"], "--file", str(ROOT / item["file"]), msg]
    log = WORK / "logs" / f"{item['wp']}.log"
    try:
        p = subprocess.run(cmd, cwd=ROOT, capture_output=True, text=True, encoding="utf-8", errors="replace", timeout=5400)
        out = (p.stdout or "") + "\n" + (p.stderr or "")
        rc = p.returncode
    except subprocess.TimeoutExpired as e:
        out, rc = f"timeout {e}", 124
    with open(log, "a", encoding="utf-8") as f:
        f.write(f"\n===== {time.strftime('%H:%M:%S')} rc={rc}\n{out[-20000:]}")
    return rc, out

def run_queue(items, cap, fanout, runner=oc_runner, base=ROOT, status_path=WORK / "status.json",
              backoff=(30, 120, 300), guard=quota_state):
    status = read_json(status_path, {}) or {}
    lock = threading.Lock()
    budget = Budget(cap)
    stop = threading.Event()

    def save():
        with lock:
            write_json(status_path, status)

    def done(item):
        return all((Path(base) / e).exists() for e in item.get("expect", []))

    def work(item):
        wp = item["wp"]
        w = min(cap, 1 + fanout) if item.get("fanout") else 1
        requeued = False
        while not stop.is_set():
            g = guard()
            if g[0] == "stop":
                stop.set(); status[wp] = {"state": "PAUSED_QUOTA", "resets": g[1]}; save(); return
            if g[0] == "wait":
                time.sleep(min(g[1], 900)); continue
            budget.acquire(w)
            try:
                status[wp] = {"state": "RUNNING", "tries": status.get(wp, {}).get("tries", 0) + 1}; save()
                rc, out = runner(item, fanout)
            finally:
                budget.release(w)
            if rc == 0 and done(item):
                status[wp] = {"state": "DONE", "tries": status[wp]["tries"]}; save(); budget.maybe_raise(); return
            tries = status[wp]["tries"]
            if RATE.search(out or "") and tries <= len(backoff):
                budget.lower(); time.sleep(backoff[tries - 1]); continue
            if not requeued:
                requeued = True; continue
            status[wp] = {"state": "FAILED", "tries": tries, "rc": rc}; save(); return

    todo = [i for i in items if status.get(i["wp"], {}).get("state") != "DONE"]
    with ThreadPoolExecutor(max_workers=max(1, cap)) as ex:
        list(ex.map(work, todo))
    return status

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--queue", required=True, help="B, C, D or a queue file path")
    ap.add_argument("--max", type=int, default=None, help="override measured budget (never lower it to be safe)")
    ap.add_argument("--fanout", type=int, default=None)
    ap.add_argument("--only", default=None, help="comma list of WP ids")
    a = ap.parse_args()
    cap_info = read_json(WORK / "plan" / "capacity.json", {}) or {}
    cap = a.max or cap_info.get("budget", 19)
    fan = a.fanout if a.fanout is not None else cap_info.get("fanout", 5)
    q = Path(a.queue) if a.queue.endswith(".json") else WORK / "wp" / f"queue-{a.queue}.json"
    items = json.loads(q.read_text(encoding="utf-8"))
    if a.only:
        keep = set(a.only.split(",")); items = [i for i in items if i["wp"] in keep]
    print(f"RUN queue={q.name} items={len(items)} budget={cap} fanout={fan}")
    st = run_queue(items, cap, fan)
    counts = {}
    for i in items:
        s = st.get(i["wp"], {}).get("state", "PENDING"); counts[s] = counts.get(s, 0) + 1
    print("RESULT", json.dumps(counts))
    sys.exit(3 if counts.get("PAUSED_QUOTA") else 0)

if __name__ == "__main__":
    main()
```

- [ ] **Step 4: Run the tests.** Expected: 4 new tests `OK`. The test count shown is the total so far.

---

### Task 8: Source conversion (K5, step A3)

**Files:**
- Create: `22 Microservice Realignment/compat/convert_sources.py`
- Test: `22 Microservice Realignment/compat/tests/test_convert.py`
- Output: `_work/msr/extract/**.md`, `22 Microservice Realignment/Recovery Workbench Architecture v5 Text Extract v1.md`, `22 Microservice Realignment/Recovery Workbench Temporal and Drools Design Text Extract v1.md`

- [ ] **Step 1: Write the failing test.**

```python
import tempfile, unittest
from pathlib import Path
import docx, openpyxl
from pptx import Presentation
from pptx.util import Inches
import convert_sources as cs

class TestConvert(unittest.TestCase):
    def test_all_three(self):
        with tempfile.TemporaryDirectory() as d:
            d = Path(d)
            doc = docx.Document(); doc.add_heading("Scope", 1); doc.add_paragraph("Case owner reads ACE.")
            t = doc.add_table(rows=2, cols=2); t.cell(0, 0).text = "ID"; t.cell(0, 1).text = "Text"
            t.cell(1, 0).text = "BR-001"; t.cell(1, 1).text = "One case"; doc.save(d / "a.docx")
            prs = Presentation(); s = prs.slides.add_slide(prs.slide_layouts[5]); s.shapes.title.text = "19 services"
            tb = s.shapes.add_textbox(Inches(1), Inches(2), Inches(4), Inches(1)); tb.text_frame.text = "rwb-case owns rwb_case"
            prs.save(d / "b.pptx")
            wb = openpyxl.Workbook(); ws = wb.active; ws.title = "Log"; ws.append(["ID", "Decision"]); ws.append(["D-RCV-36", "Drools"]); wb.save(d / "c.xlsx")
            out = d / "out"
            for f in ["a.docx", "b.pptx", "c.xlsx"]:
                cs.convert(d / f, out)
            a = (out / "a.md").read_text(encoding="utf-8"); b = (out / "b.md").read_text(encoding="utf-8"); c = (out / "c.md").read_text(encoding="utf-8")
            self.assertIn("# Scope", a); self.assertIn("| BR-001 | One case |", a)
            self.assertIn("## Slide 1: 19 services", b); self.assertIn("rwb-case owns rwb_case", b)
            self.assertIn("## Sheet: Log", c); self.assertIn("| D-RCV-36 | Drools |", c)
```

- [ ] **Step 2: Run the test.** Expected: FAIL (import error).

- [ ] **Step 3: Write `convert_sources.py`.**

```python
"""docx/pptx/xlsx/md/sql/yaml -> markdown. Replaces textutil (macOS) and the Anthropic docx/pptx/xlsx skills."""
import argparse, shutil, sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
from common import ROOT, R22, WORK, latest_path, header

def _cell(s):
    return " ".join(str(s if s is not None else "").split()).replace("|", "\\|")

def _table(rows):
    rows = [r for r in rows if any(str(c or "").strip() for c in r)]
    if not rows:
        return ""
    w = max(len(r) for r in rows)
    rows = [list(r) + [""] * (w - len(r)) for r in rows]
    out = ["| " + " | ".join(_cell(c) for c in rows[0]) + " |", "|" + "---|" * w]
    out += ["| " + " | ".join(_cell(c) for c in r) + " |" for r in rows[1:]]
    return "\n".join(out) + "\n"

def docx_to_md(p):
    import docx
    from docx.table import Table
    from docx.text.paragraph import Paragraph
    d = docx.Document(p); out = []
    for el in d.element.body.iterchildren():
        tag = el.tag.rsplit("}", 1)[-1]
        if tag == "p":
            para = Paragraph(el, d); txt = para.text.strip()
            if not txt:
                continue
            st = (para.style.name or "").lower()
            if st.startswith("heading"):
                lvl = int("".join(ch for ch in st if ch.isdigit()) or 1)
                out.append("#" * min(lvl, 6) + " " + txt)
            elif st == "title":
                out.append("# " + txt)
            elif "list" in st:
                out.append("- " + txt)
            else:
                out.append(txt)
        elif tag == "tbl":
            t = Table(el, d)
            out.append(_table([[c.text for c in r.cells] for r in t.rows]))
    return "\n\n".join(out) + "\n"

def pptx_to_md(p):
    from pptx import Presentation
    prs = Presentation(p); out = []
    for i, s in enumerate(prs.slides, 1):
        title = s.shapes.title.text.strip() if s.shapes.title is not None and s.shapes.title.has_text_frame else ""
        out.append(f"## Slide {i}: {title}".rstrip(": "))
        def walk(shapes):
            for sh in shapes:
                if sh.shape_type == 6 and hasattr(sh, "shapes"):
                    walk(sh.shapes); continue
                if getattr(sh, "has_table", False) and sh.has_table:
                    out.append(_table([[c.text for c in r.cells] for r in sh.table.rows]))
                elif sh.has_text_frame and sh != s.shapes.title:
                    t = "\n".join(pp.text for pp in sh.text_frame.paragraphs if pp.text.strip())
                    if t.strip():
                        out.append(t)
        walk(s.shapes)
        if s.has_notes_slide and s.notes_slide.notes_text_frame.text.strip():
            out.append("Notes: " + s.notes_slide.notes_text_frame.text.strip())
    return "\n\n".join(out) + "\n"

def xlsx_to_md(p, max_rows=5000):
    import openpyxl
    wb = openpyxl.load_workbook(p, read_only=True, data_only=True); out = []
    for ws in wb.worksheets:
        rows = [list(r) for _, r in zip(range(max_rows), ws.iter_rows(values_only=True))]
        out.append(f"## Sheet: {ws.title}\n\n" + _table(rows))
    return "\n".join(out)

def convert(src, outdir):
    src, outdir = Path(src), Path(outdir); outdir.mkdir(parents=True, exist_ok=True)
    ext = src.suffix.lower(); dst = outdir / (src.stem + ".md")
    if ext == ".docx":
        dst.write_text(docx_to_md(src), encoding="utf-8")
    elif ext == ".pptx":
        dst.write_text(pptx_to_md(src), encoding="utf-8")
    elif ext in (".xlsx", ".xlsm"):
        dst.write_text(xlsx_to_md(src), encoding="utf-8")
    elif ext in (".md", ".txt", ".sql", ".yaml", ".yml", ".json", ".csv"):
        dst = outdir / src.name; shutil.copy2(src, dst)
    else:
        return None
    return dst

def convert_any(src, outdir):
    src = Path(src)
    if src.is_dir():
        return [convert(f, Path(outdir) / src.name / f.parent.relative_to(src)) for f in sorted(src.rglob("*")) if f.is_file()]
    return [convert(src, outdir)]

A3 = [  # (folder, family stem, kind) ; kind: file|dir
    ("Proposed Arch", "Recovery Microservice Architecture", "file"),
    ("03 Requirements and specifications", "Recovery Workbench Business Requirements Program", "file"),
    ("03 Requirements and specifications", "Recovery Workbench Business Requirements Epic 1", "file"),
    ("03 Requirements and specifications", "Recovery Workbench Business Requirements Epic 2", "file"),
    ("03 Requirements and specifications", "Recovery Workbench Lean BRD Epic 1", "file"),
    ("03 Requirements and specifications", "Recovery Workbench Lean BRD Epic 2", "file"),
    ("03 Requirements and specifications", "Recovery Workbench Epics 3 to 8 Specification", "file"),
    ("03 Requirements and specifications", "Recovery Workbench Non Functional Specification", "file"),
    ("03 Requirements and specifications", "Recovery Workbench Functional Specifications by Module", "dir"),
    ("05 Technical architecture", "Recovery Workbench Technical Specifications by Module", "dir"),
    ("05 Technical architecture", "Recovery Workbench Architecture Decision Records", "file"),
    ("05 Technical architecture", "Recovery Workbench Event and Messaging Design", "file"),
    ("05 Technical architecture", "Recovery Workbench Batch and Scheduling Design", "file"),
    ("05 Technical architecture", "Recovery Workbench API Specification", "file"),
    ("02 Business architecture and process", "Recovery Workbench Business Rules and Routing Logic", "file"),
    ("06 Data", "Recovery Workbench Physical Schema", "file"),
    ("06 Data", "Recovery Workbench Logical Data Model and Data Dictionary", "file"),
    ("01 Decisions and governance", "Recovery Workbench Decision Log", "file"),
]

def run_a3():
    ex = WORK / "extract"; done = []
    for folder, stem, kind in A3:
        p = latest_path(ROOT / folder, stem, "dir" if kind == "dir" else None)
        if p is not None and kind == "file" and p.is_dir():
            p = latest_path(ROOT / folder, stem, ".docx") or latest_path(ROOT / folder, stem, ".md") or p
        if p is None:
            print("MISSING", folder, stem); continue
        done += [x for x in convert_any(p, ex) if x]
    for src, title, name in [
        (ROOT / "Proposed Arch" / "Recovery Microservice Architecture v5.pptx", "Architecture v5 Text Extract", "Recovery Workbench Architecture v5 Text Extract v1.md"),
        (ROOT / "Proposed Arch" / "Recovery Temporal and Drools Detailed Design v1.pptx", "Temporal and Drools Design Text Extract", "Recovery Workbench Temporal and Drools Design Text Extract v1.md")]:
        body = pptx_to_md(src)
        (R22 / name).write_text(f"# Recovery Workbench {title} v1\n\n{header()}\nSource: `{src.relative_to(ROOT)}` (read-only).\n\n{body}", encoding="utf-8")
        (ex / name).write_text(body, encoding="utf-8")
    print(f"A3 OK {len(done)} files converted into {ex}")

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("src", nargs="?"); ap.add_argument("outdir", nargs="?")
    ap.add_argument("--a3", action="store_true")
    a = ap.parse_args()
    if a.a3:
        run_a3()
    else:
        for x in convert_any(a.src, a.outdir):
            print("WROTE", x)

if __name__ == "__main__":
    main()
```

- [ ] **Step 4: Run the tests, then step A3.**

```powershell
python -I "22 Microservice Realignment/compat/convert_sources.py" --a3
```

Expected: tests OK, then `A3 OK <n> files converted`. Any `MISSING` line becomes an ASM, written to `_work/msr/assumptions/A3.jsonl`. Both Text Extract files now exist in folder 22.

---

### Task 9: Legacy story index (step A4)

**Files:**
- Create: `22 Microservice Realignment/compat/legacy_index.py`
- Test: `22 Microservice Realignment/compat/tests/test_legacy_index.py`
- Output: `_work/msr/plan/legacy_index.json`, `_work/msr/plan/legacy_hashes.json`

- [ ] **Step 1: Write the failing test.**

```python
import tempfile, unittest
from pathlib import Path
import legacy_index as li

MASTER = """# Recovery Workbench User Stories Epics 3 to 8 v3

## RWB-E4-001 Order an appraisal when the last one is stale

| Item | Value |
|---|---|
| Epic | E4, release 28 February 2027 |
| Module | S1 Valuation and route |
| Depends on | RWB-E1-018, FEAT-RDF-06 |
| Requirement IDs | REQ-VAL-001 |

**Story.** As a case owner, I want ...

**Acceptance criteria**

~~~gherkin
  Scenario: AC1 Order an appraisal
    Given x
  Scenario: AC2 Not recorded
    Then the user sees MSG-P7-003
~~~

| ID | Covers | Level | Data |
|---|---|---|---|
| TC-E4-001-01 | AC1 | API | x |

## RWB-E4-002 Second

| Item | Value |
|---|---|
| Epic | E4, release 28 February 2027 |
| Module | S1 Valuation and route |
| Depends on | None |
"""

class TestIndex(unittest.TestCase):
    def test_parse(self):
        with tempfile.TemporaryDirectory() as d:
            p = Path(d) / "m.md"; p.write_text(MASTER, encoding="utf-8")
            rows = li.parse_master(p, "E3-8")
            self.assertEqual([r["key"] for r in rows], ["RWB-E4-001", "RWB-E4-002"])
            r = rows[0]
            self.assertEqual(r["module"], "S1"); self.assertEqual(r["release"], "28 February 2027")
            self.assertEqual(r["deps"], ["RWB-E1-018"]); self.assertEqual(r["feat_deps"], ["FEAT-RDF-06"])
            self.assertEqual(r["acs"], ["AC1", "AC2"]); self.assertEqual(r["tcs"], ["TC-E4-001-01"])
            self.assertEqual(r["reqs"], ["REQ-VAL-001"]); self.assertEqual(r["business_epic"], "EP04")
            self.assertIn("Story", r["sections"]); self.assertEqual(len(r["sha256"]), 64)
            self.assertEqual(rows[1]["deps"], [])
```

- [ ] **Step 2: Run the test.** Expected: FAIL (import error).

- [ ] **Step 3: Write `legacy_index.py`.**

```python
"""Parse the 7 legacy story masters (+ E1/E2 story files) into _work/msr/plan/legacy_index.json."""
import hashlib, re, sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
from common import STORIES, WORK, LEGACY_RE, sha256, write_json, append_jsonl

MASTERS = [  # file, group, expected count
    ("Recovery Workbench User Stories Epic 1 v9.md", "E1", 72),
    ("Recovery Workbench User Stories Epic 2 v7.md", "E2", 41),
    ("Recovery Workbench User Stories Epics 3 to 8 v3.md", "E3-8", 181),
    ("Recovery Workbench Technical Enabler Stories v7.md", "TE", 12),
    ("Recovery Workbench Administration Stories v3.md", "AD", 22),
    ("Recovery Workbench Data Migration Stories v3.md", "DM", 14),
    ("Recovery Workbench ACE Team Stories v1.md", "ACE", 1),
]
STORY_DIRS = {"E1": "Recovery Workbench User Stories Epic 1 Story Files v7", "E2": "Recovery Workbench User Stories Epic 2 Story Files v5"}
HEAD = re.compile(r"^#{1,2} (RWB-(?:E[1-8]|TE|AD|DM|ACE)-\d{3})\b[ \t]*(.*)$", re.M)
META = re.compile(r"^\|\s*([^|]+?)\s*\|\s*(.*?)\s*\|\s*$", re.M)
SEC_NUM = re.compile(r"^### (\d+)\. (.+)$", re.M)
SEC_BOLD = re.compile(r"^\*\*([A-Z][^*\n]{1,60}?)\.?\*\*", re.M)
BE = {"E1": "EP01", "TE": "EP01-TE", "ACE": "EP01", "E2": "EP02", "E3": "EP03", "E4": "EP04", "E5": "EP05",
      "E6": "EP06", "E7": "EP07", "E8": "EP08", "AD": "EP08", "DM": "EP08"}
NF = {  # Non feature tasks (no master; titles from the realignment plan, gaps raised in split_plan)
    "NF-01": "Repository and pipeline baseline", "NF-02": "Shared library baseline", "NF-03": "Environment baseline",
    "NF-04": "Secrets and configuration baseline", "NF-05": "Quality gates baseline",
    "NF-06": "Create the 19 rwb_* schemas and logins", "NF-07": "Airflow edge integration", "NF-08": "Temporal platform baseline"}

def _meta(block):
    out = {}
    for k, v in META.findall(block.split("\n### ", 1)[0].split("**Story", 1)[0]):
        if k not in ("Item", "---") and not set(k) <= set("-: "):
            out.setdefault(k, v)
    return out

def _sections(block):
    hits = [(m.start(), m.group(2).strip()) for m in SEC_NUM.finditer(block)]
    if not hits:
        hits = [(m.start(), m.group(1).strip()) for m in SEC_BOLD.finditer(block)]
    secs = {}
    for i, (pos, name) in enumerate(hits):
        end = hits[i + 1][0] if i + 1 < len(hits) else len(block)
        secs[name] = block[pos:end]
    return secs

def _uniq(xs):
    seen = []
    for x in xs:
        if x not in seen:
            seen.append(x)
    return seen

def parse_master(path, group):
    text = Path(path).read_text(encoding="utf-8")
    heads = list(HEAD.finditer(text)); rows = []
    for i, m in enumerate(heads):
        block = text[m.start(): heads[i + 1].start() if i + 1 < len(heads) else len(text)]
        meta = _meta(block); key = m.group(1)
        epic_row = meta.get("Epic", "")
        rel = re.search(r"release\s+(.+)$", epic_row)
        mod = re.match(r"\s*(P10|P[1-9]|S[1-9])\b", meta.get("Module", ""))
        pfx = key.split("-")[1]
        em = re.match(r"\s*(E[1-8])\b", epic_row)
        be = BE.get(pfx if pfx in ("TE", "ACE", "AD", "DM") else (em.group(1) if em else pfx), "EP08")
        deps_txt = meta.get("Depends on", "")
        rows.append({
            "key": key, "title": m.group(2).strip(), "group": group, "master": str(Path(path).name),
            "meta": meta, "module": mod.group(1) if mod else None, "release": rel.group(1).strip() if rel else "",
            "business_epic": be,
            "deps": _uniq(f"RWB-{a}-{b}" for a, b in LEGACY_RE.findall(deps_txt) if f"RWB-{a}-{b}" != key),
            "feat_deps": _uniq(re.findall(r"FEAT-[A-Z]+-\d+", deps_txt)),
            "reqs": _uniq(re.findall(r"REQ-[A-Z]+-\d{3}", block)),
            "acs": _uniq(re.findall(r"Scenario:\s*(AC\d+)", block)),
            "tcs": _uniq(re.findall(r"\bTC-[A-Z0-9]+-\d{3}-\d{2}\b", block)),
            "msgs": _uniq(re.findall(r"\bMSG-[A-Z0-9]+-\d{3}\b", block)),
            "sections": {k: len(v) for k, v in _sections(block).items()},
            "status": meta.get("Status", ""),
            "chars": len(block),
            "sha256": hashlib.sha256(block.encode("utf-8")).hexdigest(),
            "story_file": None, "story_file_sha256": None,
        })
    return rows

def attach_story_files(rows):
    for grp, folder in STORY_DIRS.items():
        d = STORIES / folder
        files = {f.name: f for f in d.glob("*.md")} if d.exists() else {}
        for r in rows:
            if r["group"] != grp:
                continue
            k = r["key"].replace("RWB-", "RWB ").replace("-", " ")  # RWB E1 018
            hit = next((f for n, f in sorted(files.items()) if n.startswith(k + " ")), None)
            if hit:
                r["story_file"] = str(hit.relative_to(STORIES.parent)); r["story_file_sha256"] = sha256(hit)

def main():
    rows, counts = [], {}
    for fname, grp, exp in MASTERS:
        part = parse_master(STORIES / fname, grp); rows += part; counts[grp] = (len(part), exp)
        if len(part) != exp:
            append_jsonl(WORK / "assumptions" / "A4.jsonl", {"id": f"ASM-A4-{grp}", "text": f"{fname} has {len(part)} story headings, plan expected {exp}; the parsed count is used.", "why": "count differs", "read": fname, "confidence": "High"})
    for k, t in NF.items():
        rows.append({"key": k, "title": t, "group": "NF", "master": None, "meta": {}, "module": None, "release": "",
                     "business_epic": "NF", "deps": [], "feat_deps": [], "reqs": [], "acs": [], "tcs": [], "msgs": [],
                     "sections": {}, "status": "", "chars": 0, "sha256": None, "story_file": None, "story_file_sha256": None})
    attach_story_files(rows)
    write_json(WORK / "plan" / "legacy_index.json", rows)
    hashes = {fname: sha256(STORIES / fname) for fname, _, _ in MASTERS}
    hashes.update({r["story_file"]: r["story_file_sha256"] for r in rows if r["story_file"]})
    write_json(WORK / "plan" / "legacy_hashes.json", hashes)
    print("A4 OK", {g: c[0] for g, c in counts.items()}, "total", len(rows))

if __name__ == "__main__":
    main()
```

- [ ] **Step 4: Run the tests, then step A4.**

```powershell
python -I "22 Microservice Realignment/compat/legacy_index.py"
```

Expected: `A4 OK {'E1': 72, 'E2': 41, 'E3-8': 181, 'TE': 12, 'AD': 22, 'DM': 14, 'ACE': 1} total 351`. The total is 343 stories plus 8 NF. Each count that differs gets an `ASM-A4-*` row; the run continues regardless.

---

### Task 10: ID collision scan (step A5)

**Files:**
- Create: `22 Microservice Realignment/compat/id_scan.py`
- Output: `_work/msr/plan/ids.json`

- [ ] **Step 1: Write `id_scan.py`.**

```python
"""Find used D-RCV / ADR / DL numbers across the set (md, extracts, xlsx) and allocate free ones."""
import re, sys
from pathlib import Path
import openpyxl
sys.path.insert(0, str(Path(__file__).resolve().parent))
from common import ROOT, WORK, write_json

PAT = {"drcv": re.compile(r"\bD-RCV-(\d{2,3})\b"), "adr": re.compile(r"\bADR-(\d{3})\b"), "dl": re.compile(r"\bDL(\d{2,3})\b")}
WANT = {"drcv": [53], "adr": list(range(13, 24)), "dl": list(range(44, 50))}
SKIP = {"_work", ".git", "node_modules", "temp", "rwb-wt"}

def scan():
    used = {k: set() for k in PAT}
    for p in ROOT.rglob("*"):
        if any(part in SKIP for part in p.parts) or not p.is_file():
            continue
        try:
            if p.suffix.lower() in (".md", ".txt", ".yaml", ".yml", ".sql", ".json"):
                txt = p.read_text(encoding="utf-8", errors="ignore")
            elif p.suffix.lower() == ".xlsx" and "Decision" in p.name:
                wb = openpyxl.load_workbook(p, read_only=True, data_only=True)
                txt = " ".join(str(c) for ws in wb.worksheets for r in ws.iter_rows(values_only=True) for c in r if c)
            else:
                continue
        except Exception:
            continue
        for k, rx in PAT.items():
            used[k].update(int(x) for x in rx.findall(txt))
    for p in (WORK / "extract").rglob("*.md"):
        txt = p.read_text(encoding="utf-8", errors="ignore")
        for k, rx in PAT.items():
            used[k].update(int(x) for x in rx.findall(txt))
    return used

def allocate(used, want):
    out, nxt = [], (max(used) + 1 if used else want[0])
    for w in want:
        if w in used or w in out:
            while nxt in used or nxt in out:
                nxt += 1
            out.append(nxt); nxt += 1
        else:
            out.append(w)
    return out

def main():
    used = scan()
    ids = {k: allocate(used[k], WANT[k]) for k in PAT}
    res = {"realignment_decision": f"D-RCV-{ids['drcv'][0]}", "adrs": [f"ADR-{n:03d}" for n in ids["adr"]],
           "dl": [f"DL{n}" for n in ids["dl"]], "max_used": {k: max(v) if v else 0 for k, v in used.items()},
           "collisions": {k: sorted(set(WANT[k]) & used[k]) for k in PAT}}
    write_json(WORK / "plan" / "ids.json", res)
    print("A5 OK", res["realignment_decision"], res["adrs"][0], "..", res["adrs"][-1], res["dl"][0], "..", res["dl"][-1], "collisions", res["collisions"])

if __name__ == "__main__":
    main()
```

- [ ] **Step 2: Run the scan.**

```powershell
python -I "22 Microservice Realignment/compat/id_scan.py"
```

Expected: `A5 OK D-RCV-53 ADR-013 .. ADR-023 DL44 .. DL49 collisions {'drcv': [], 'adr': [], 'dl': []}`.

If the collision lists are not empty, every later file uses the allocated IDs from `ids.json`, not the numbers written in this plan. Also add a candidate gap of type "ID collision" (P3) to `_work/msr/gaps/A5.jsonl`; the row format is in Task 15.

---

### Task 11: Ownership Map v1 (step A6, run as 3 parallel agent WPs)

**Files:**
- Create: `22 Microservice Realignment/compat/ownership.py`
- Create: `22 Microservice Realignment/compat/xlsx_write.py`
- Output:
  - `_work/msr/plan/ownership_skeleton.json`
  - `_work/msr/plan/ownership_part_{tables,api,flows}.json`, one per agent
  - `_work/msr/plan/ownership.json`
  - `22 Microservice Realignment/Recovery Workbench Microservice Ownership Map v1.xlsx`

- [ ] **Step 1: Write `xlsx_write.py`.** Every script that writes an xlsx uses it.

```python
from pathlib import Path
from openpyxl import Workbook
from openpyxl.styles import Alignment, Font, PatternFill
from openpyxl.utils import get_column_letter

HEAD_FILL = PatternFill("solid", fgColor="1F3864")

def write_book(path, sheets, read_me=None):
    """sheets: dict name -> (header list, rows list). Header row bold white on navy, freeze, filter."""
    wb = Workbook(); wb.remove(wb.active)
    if read_me:
        ws = wb.create_sheet("Read me")
        for line in read_me.splitlines():
            ws.append([line])
        ws.column_dimensions["A"].width = 120
    for name, (head, rows) in sheets.items():
        ws = wb.create_sheet(name[:31]); ws.append(head)
        for c in ws[1]:
            c.font = Font(bold=True, color="FFFFFF"); c.fill = HEAD_FILL; c.alignment = Alignment(wrap_text=True, vertical="top")
        for r in rows:
            ws.append([("; ".join(map(str, v)) if isinstance(v, (list, tuple, set)) else v) for v in r])
        ws.freeze_panes = "A2"
        if rows:
            ws.auto_filter.ref = ws.dimensions
        for i, h in enumerate(head, 1):
            ws.column_dimensions[get_column_letter(i)].width = min(60, max(12, len(str(h)) + 4))
    Path(path).parent.mkdir(parents=True, exist_ok=True)
    wb.save(path)
    return path
```

- [ ] **Step 2: Write `ownership.py`.** It has three subcommands: `skeleton`, `wps` and `merge`.

```python
"""Ownership Map: skeleton from the sources -> 3 agent WPs decide owners by R-PREC -> merge + validate + xlsx."""
import argparse, collections, json, re, sys
from pathlib import Path
import yaml
sys.path.insert(0, str(Path(__file__).resolve().parent))
from common import ROOT, R22, WORK, SERVICES, latest_path, read_json, write_json, header, append_jsonl
from xlsx_write import write_book

CODES = [s["code"] for s in SERVICES] + ["PLT"]
DEFAULT_RULINGS = [  # R-PREC default rulings (Appendix R §R3); each is also an assumption
    ("parameters and reference data (E1-042, E1-043)", "P3"), ("case list API", "P3"),
    ("rule package registry", "P7"), ("interaction ledger", "P1"), ("feature flags", "PLT")]

def _sql_tables():
    p = latest_path(ROOT / "06 Data", "Recovery Workbench Physical Schema", ".sql")
    if p is None:
        d = latest_path(ROOT / "06 Data", "Recovery Workbench Physical Schema", "dir")
        p = next(iter(sorted(d.rglob("*.sql")))) if d else None
    txt = p.read_text(encoding="utf-8", errors="ignore") if p else ""
    return sorted(set(re.findall(r"(?i)create\s+table\s+(?:if\s+not\s+exists\s+)?(?:\"?recovery\"?\.)?\"?(\w+)\"?", txt))), (str(p.relative_to(ROOT)) if p else None)

def _api_ops():
    ops = []
    for p in sorted(ROOT.joinpath("05 Technical architecture").rglob("*.yaml")):
        if "API Specification" not in str(p):
            continue
        try:
            d = yaml.safe_load(p.read_text(encoding="utf-8", errors="ignore")) or {}
        except Exception:
            continue
        for path, item in (d.get("paths") or {}).items():
            for m, op in (item or {}).items():
                if isinstance(op, dict) and m.lower() in ("get", "post", "put", "patch", "delete"):
                    ops.append({"method": m.upper(), "path": path, "operationId": op.get("operationId"),
                                "x_module": op.get("x-module") or item.get("x-module"), "file": str(p.relative_to(ROOT))})
    return ops

def _ids(rx):
    found = collections.Counter()
    for p in (WORK / "extract").rglob("*.md"):
        found.update(re.findall(rx, p.read_text(encoding="utf-8", errors="ignore")))
    return sorted(found)

def skeleton():
    tables, schema_file = _sql_tables()
    idx = read_json(WORK / "plan" / "legacy_index.json", [])
    hint = collections.defaultdict(collections.Counter)
    masters = {}
    for r in idx:
        if not r.get("master") or not r.get("module"):
            continue
        if r["master"] not in masters:
            masters[r["master"]] = (ROOT / "04 User stories" / r["master"]).read_text(encoding="utf-8", errors="ignore")
    text_by_module = collections.defaultdict(str)
    for r in idx:
        if r.get("master") and r.get("module"):
            t = masters[r["master"]]; i = t.find(r["key"]); text_by_module[r["module"]] += t[i:i + r["chars"]]
    for t in tables:
        rx = re.compile(r"\b" + re.escape(t) + r"\b")
        for mod, txt in text_by_module.items():
            n = len(rx.findall(txt))
            if n:
                hint[t][mod] = n
    sk = {"schema_file": schema_file,
          "tables": [{"table": t, "hint": dict(hint[t].most_common(3))} for t in tables],
          "api": _api_ops(), "events": _ids(r"\bEV-\d{2,3}\b"), "jobs": _ids(r"\bJOB-\d{2,3}\b"),
          "workflows": _ids(r"\b[A-Z][A-Za-z]+Workflow\b"), "rulings": DEFAULT_RULINGS}
    write_json(WORK / "plan" / "ownership_skeleton.json", sk)
    print(f"SKELETON tables={len(tables)} api_ops={len(sk['api'])} events={len(sk['events'])} jobs={len(sk['jobs'])} workflows={len(sk['workflows'])}")

WP_TEXT = """# WP A6-{part} — Ownership Map part: {part}
Tool rules: AGENTS.md (root) rules 1-14. Agent: aisdlc-msr-worker. fanout: 0
Read only:
- _work/msr/plan/ownership_skeleton.json (section "{key}")
- 22 Microservice Realignment/Recovery Workbench Architecture v5 Text Extract v1.md (catalogue slides 14-20 and 41-44 win over narrative slides)
- 22 Microservice Realignment/Recovery Workbench Temporal and Drools Design Text Extract v1.md
- _work/msr/extract/ (FSD v6 and TSD v5 module files, Event and Messaging, Batch and Scheduling, Physical Schema)
- The R-PREC precedence and default rulings in 2026-11-22-recovery-microservice-realignment-implementation-plan.md Appendix R §R3
Write only: _work/msr/plan/ownership_part_{part}.json ; _work/msr/gaps/A6-{part}.jsonl ; _work/msr/assumptions/A6-{part}.jsonl ; _work/msr/editlog/A6-{part}.md
Do: for EVERY item in the skeleton section, choose exactly one owner from {codes}. Use R-PREC order. The "hint" counts are which legacy module stories mention the table (a hint, not a rule).
Output JSON: {{"{key}": [{{"id": "<table | METHOD path | EV-nn | JOB-nn | Workflow>", "owner": "<code>", "basis": "<source file + slide/section>", "ruling": "<text or empty>", "asm": "<ASM-A6-{part}-n or empty>"}}]}}
Every ruling (two sources disagree) also gets a gap row (type Conflict, severity P2) and an assumption row.
Jobs: also give "replacement": "Temporal Schedule <name> in <service>" or "event-started workflow" (v5 slide 44); Quartz is retired.
Finish: every skeleton item appears once in your output. Write the edit log with tool line T3 Code / OpenCode / DeepSeek v4.1 Flash.
"""

def wps():
    parts = {"tables": "tables", "api": "api", "flows": "events, jobs, workflows"}
    q = []
    for part, key in parts.items():
        f = WORK / "wp" / f"A6-{part}.md"
        f.write_text(WP_TEXT.format(part=part, key=key, codes=", ".join(CODES)), encoding="utf-8")
        q.append({"wp": f"A6-{part}", "agent": "aisdlc-msr-worker", "file": str(f.relative_to(ROOT)), "fanout": False,
                  "expect": [f"_work/msr/plan/ownership_part_{part}.json"]})
    write_json(WORK / "wp" / "queue-A6.json", q)
    print("WPS A6 written: 3")

def merge():
    sk = read_json(WORK / "plan" / "ownership_skeleton.json")
    om = {"tables": {}, "api": {}, "events": {}, "jobs": {}, "workflows": {}, "rulings": []}
    for part in ("tables", "api", "flows"):
        d = read_json(WORK / "plan" / f"ownership_part_{part}.json", {}) or {}
        for key, rows in d.items():
            for r in rows if isinstance(rows, list) else []:
                k = key if key in om else ("events" if str(r.get("id", "")).startswith("EV-") else "jobs" if str(r.get("id", "")).startswith("JOB-") else "workflows")
                om[k][r["id"]] = r
                if r.get("ruling"):
                    om["rulings"].append([r["id"], r["owner"], r["ruling"], r.get("asm", "")])
    bad = []
    for t in sk["tables"]:
        o = om["tables"].get(t["table"], {}).get("owner")
        if o not in CODES:
            hint = max(t["hint"], key=t["hint"].get) if t["hint"] else "P3"
            om["tables"][t["table"]] = {"id": t["table"], "owner": hint, "basis": "fallback: most frequent legacy module", "ruling": "", "asm": "ASM-A6-fallback"}
            bad.append(t["table"])
    if bad:
        append_jsonl(WORK / "assumptions" / "A6-merge.jsonl", {"id": "ASM-A6-merge-1", "text": f"{len(bad)} tables had no agent owner; owner set to the most frequent legacy module: {', '.join(bad[:40])}", "why": "agent output missing", "read": "ownership_skeleton.json", "confidence": "Low"})
    for name, owner in DEFAULT_RULINGS:
        om["rulings"].append([name, owner, "R-PREC default ruling", "ASM-seed"])
    write_json(WORK / "plan" / "ownership.json", om)
    fk = fk_cuts(om)
    s = {s_["code"]: s_ for s_ in SERVICES}
    write_book(R22 / "Recovery Workbench Microservice Ownership Map v1.xlsx", {
        "Services": (["Code", "Service", "Name", "Wave", "Schema", "REST base", "Topic", "Queue"], [[x["code"], x["service"], x["name"], x["wave"], x["schema"], x["base"], x["topic"], x["queue"]] for x in SERVICES]),
        "Tables": (["Table", "Owner", "Schema", "Basis", "Ruling", "Assumption"], [[k, v["owner"], s[v["owner"]]["schema"] if v["owner"] in s else "platform", v.get("basis"), v.get("ruling"), v.get("asm")] for k, v in sorted(om["tables"].items())]),
        "FK cuts": (["From table", "From owner", "To table", "To owner", "Becomes"], fk),
        "Endpoints": (["Operation", "Owner", "Basis", "Ruling"], [[k, v["owner"], v.get("basis"), v.get("ruling")] for k, v in sorted(om["api"].items())]),
        "Events": (["Event", "Owner", "Basis", "Ruling"], [[k, v["owner"], v.get("basis"), v.get("ruling")] for k, v in sorted(om["events"].items())]),
        "Workflows and activities": (["Workflow", "Owner", "Basis"], [[k, v["owner"], v.get("basis")] for k, v in sorted(om["workflows"].items())]),
        "Jobs": (["Job", "Owner", "Replacement", "Basis"], [[k, v["owner"], v.get("replacement"), v.get("basis")] for k, v in sorted(om["jobs"].items())]),
        "Parameters": (["Item", "Owner", "Note"], [["parameters", "P3", "rwb-case contract RWB-P3-E1042-CON"], ["reference data", "P3", "rwb-case contract RWB-P3-E1043-CON"]]),
        "Rulings": (["Item", "Owner", "Ruling", "Assumption"], om["rulings"]),
    }, read_me=header() + "\nRecovery Workbench Microservice Ownership Map v1 (D-RCV-53). Generated by compat/ownership.py merge.\nTool: T3 Code / OpenCode / DeepSeek v4.1 Flash.")
    print(f"MERGE OK tables={len(om['tables'])} api={len(om['api'])} events={len(om['events'])} jobs={len(om['jobs'])} fallback={len(bad)} fk_cuts={len(fk)}")

def fk_cuts(om):
    sk = read_json(WORK / "plan" / "ownership_skeleton.json")
    p = ROOT / sk["schema_file"] if sk.get("schema_file") else None
    txt = p.read_text(encoding="utf-8", errors="ignore") if p and p.exists() else ""
    rows = []
    for m in re.finditer(r"(?is)create\s+table\s+(?:if\s+not\s+exists\s+)?(?:\"?recovery\"?\.)?\"?(\w+)\"?\s*\((.*?)\n\);", txt):
        src = m.group(1)
        for tgt in re.findall(r"(?i)references\s+(?:\"?recovery\"?\.)?\"?(\w+)", m.group(2)):
            a = om["tables"].get(src, {}).get("owner"); b = om["tables"].get(tgt, {}).get("owner")
            if a and b and a != b:
                rows.append([src, a, tgt, b, "plain uuid column; integrity through the owner's contract"])
    return rows

if __name__ == "__main__":
    ap = argparse.ArgumentParser(); ap.add_argument("cmd", choices=["skeleton", "wps", "merge"]); a = ap.parse_args()
    {"skeleton": skeleton, "wps": wps, "merge": merge}[a.cmd]()
```

- [ ] **Step 3: Run the skeleton, the WP files and the 3 agents in parallel, then merge.** Run these four commands in order:

```powershell
python -I "22 Microservice Realignment/compat/ownership.py" skeleton
```

```powershell
python -I "22 Microservice Realignment/compat/ownership.py" wps
```

```powershell
python -I "22 Microservice Realignment/compat/run_parallel.py" --queue A6
```

```powershell
python -I "22 Microservice Realignment/compat/ownership.py" merge
```

Expected output:
1. `SKELETON tables=<about 92> api_ops=<n> …`
2. `WPS A6 written: 3`
3. `RESULT {"DONE": 3}`
4. `MERGE OK tables=<about 92> … fallback=<k>`

`fallback` above 0 is allowed: it is recorded as a Low-confidence assumption.

---

### Task 12: Classifier, split plan, dependency classes, lanes and Day-1 (step A7a)

**Files:**
- Create: `22 Microservice Realignment/compat/split_plan.py`
- Test: `22 Microservice Realignment/compat/tests/test_split_plan.py`
- Output: `_work/msr/plan/split_plan.json`, plus candidates in `_work/msr/gaps/A7.jsonl` and `_work/msr/assumptions/A7.jsonl`

The rules are in Appendix R §R5 (target structure) and §R6 (Epic 1 preservation). The script encodes them as data, so the WP agents never decide slices, IDs, dependencies or lanes.

- [ ] **Step 1: Write the failing test.**

```python
import unittest
import split_plan as sp
from common import ID_RE

def row(key, module, deps=(), be="EP01", group="E1"):
    return {"key": key, "title": f"Title {key}", "group": group, "master": "m.md", "module": module, "release": "30 November 2026",
            "business_epic": be, "deps": list(deps), "reqs": [], "acs": [], "tcs": [], "story_file": None}

class TestSplit(unittest.TestCase):
    def setUp(self):
        chain = [row(f"RWB-E1-1{i:02d}", "P3", deps=[f"RWB-E1-1{i-1:02d}"] if i else []) for i in range(7)]
        self.index = chain + [
            row("RWB-E1-014", "P9"), row("RWB-E1-042", "P3"), row("RWB-TE-001", None, group="TE", be="EP01-TE"),
            row("RWB-E1-016", "P1"), row("RWB-E1-200", "P3", deps=["RWB-E1-016", "RWB-E1-014", "RWB-TE-007"]),
            row("RWB-E1-027", "P7"), row("RWB-E1-071", "P3"), row("NF-06", None, group="NF", be="NF")]
        self.blocks = {r["key"]: "plain text" for r in self.index}
        self.blocks["RWB-E1-016"] = "Provides GET /api/recovery/v1/accounts and EV-01. Writes account_ext (W)."
        self.blocks["RWB-E1-200"] = ("Uses DecisionLogWriter.\nScenario: AC1 Create\n Given x\n Then y\n"
                                     "Scenario: AC2 Gate\n Given the ALS batch is COMPLETED\n Then z\n")
        self.own = {"tables": {"account_ext": {"owner": "P1"}}}
        self.plan = sp.build(self.index, self.blocks, self.own)
        self.s = {x["id"]: x for x in self.plan["slices"]}

    def test_ids_valid_and_unique(self):
        ids = [x["id"] for x in self.plan["slices"]]
        self.assertEqual(len(ids), len(set(ids)))
        for i in ids:
            self.assertRegex(i, ID_RE)

    def test_retire_and_preserve(self):
        self.assertEqual(self.plan["legacy"]["RWB-E1-014"]["disposition"], "Retired (D-RCV-53)")
        self.assertIn("RWB-P3-E1042-APP", self.s); self.assertTrue(self.s["RWB-P3-E1042-APP"]["preserved"])
        self.assertIn("RWB-P3-E1042-CON", self.s); self.assertIn("RWB-PLT-E1042-CON", self.s)
        self.assertIn("RWB-PLT-TE001-APP", self.s); self.assertIn("RWB-PLT-TE001-APP-2", self.s)
        self.assertIn("RWB-PLT-NF06-DB", self.s)

    def test_dependency_classes(self):
        a = self.s["RWB-P3-E1200-APP"]
        self.assertIn("RWB-P1-E1016-CON", a["C"])            # other service with CON -> C
        self.assertIn("RWB-PLT-E1071-CON", a["H"])           # TE-007 redirect
        self.assertIn("RWB-PLT-E1027-CON", a["H"])           # DP-03
        self.assertNotIn("RWB-E1-014", str(a))               # dropped
        itg = self.s["RWB-ITG-E1200-ITG"]
        self.assertIn("AC2", itg["acs"]); self.assertIn("AC1", a["acs"])
        self.assertIn("RWB-P1-E1016-APP", itg["I"])
        for x in self.plan["slices"]:
            for h in x["H"]:
                t = self.s.get(h)
                self.assertTrue(t is not None, h)
                self.assertTrue(t["wt"] == "CON" or t["scope"] == x["scope"], (x["id"], h))
                self.assertFalse(t["scope"] == "PLT" and t["wt"] != "CON" and x["scope"] != "PLT", (x["id"], h))
            if x["scope"] != "ITG":
                self.assertEqual(x["I"], [])

    def test_lane_depth_and_day1(self):
        import networkx as nx
        g = nx.DiGraph()
        for x in self.plan["slices"]:
            if x["wt"] != "CON":
                g.add_node(x["id"])
                for h in x["H"]:
                    if self.s[h]["wt"] != "CON":
                        g.add_edge(h, x["id"])
        for comp in nx.weakly_connected_components(g):
            self.assertLessEqual(len(nx.dag_longest_path(g.subgraph(comp))), 4)
        for x in self.plan["slices"]:
            if x["wt"] == "CON":
                self.assertEqual(x["ready"], "Day 1"); self.assertEqual(x["H"], [])
        teams = {x["owner"] for x in self.plan["slices"] if x["ready"] == "Day 1"}
        self.assertTrue({"TechX", "ACE", "INFRA", "DEVOPS", "QA"} <= teams, teams)
        self.assertEqual(len([x for x in self.plan["slices"] if x["wt"] == "CON" and x["scope"] in sp.SVC_CODES]) >= 19, True)
```

- [ ] **Step 2: Run the test.** Expected: FAIL (import error).

- [ ] **Step 3: Write `split_plan.py`.**

```python
"""Deterministic split of every legacy story into service/platform/integration slices (Appendix R §R5-R6)."""
import re, string, sys
from pathlib import Path
import networkx as nx
sys.path.insert(0, str(Path(__file__).resolve().parent))
from common import (ROOT, STORIES, WORK, SERVICES, OWNER, WT_OWNER, WT_SUFFIX, svc, story_id, leg_compact,
                    read_json, write_json, reset_cands, add_gap, add_asm)

SVC_CODES = [s["code"] for s in SERVICES]
WMAP = {"EP01": 1, "EP01-TE": 1, "EP02": 2, "EP03": 2, "EP04": 3, "EP05": 3, "EP06": 4, "EP07": 4, "EP08": 4, "NF": 0, "NEW": 0}
RETIRE_NEW = {"RWB-E1-014", "RWB-TE-007"}
ALREADY = {f"RWB-E1-{n}" for n in ("003", "004", "005", "006", "009", "010", "012", "029", "048", "051")} | {"RWB-TE-005"}
PRESERVED = {"RWB-TE-001", "RWB-TE-002", "RWB-TE-003", "RWB-E1-042", "RWB-E1-043", "RWB-E1-044"}
MUST = {"RWB-E1-001"}
NO_IMPACT = {f"RWB-E1-0{n}" for n in ("24", "25", "26", "33", "34", "38", "40", "41", "45", "53", "60", "61", "68")} | {"RWB-TE-010", "RWB-TE-012"}
BUILD_STATUS = {"RWB-TE-001": "Built", "RWB-TE-002": "Built", "RWB-TE-003": "In build", "RWB-E1-042": "In build",
                "RWB-E1-043": "In build", "RWB-E1-044": "In build", "RWB-E1-001": "In build"}
PLT = {"RWB-TE-001": ("TPL", ["APP"]), "RWB-TE-002": ("TPL", ["OPS"]), "RWB-TE-003": ("TPL", ["APP"]),
       "RWB-TE-004": ("TPL", ["APP"]), "RWB-TE-006": ("LIB", ["CON", "APP"]), "RWB-TE-008": ("TPL", ["APP"]),
       "RWB-TE-011": ("TPL", ["APP"]), "RWB-TE-012": ("TPL", ["APP"]),
       "RWB-E1-027": ("LIB", ["CON", "APP"]), "RWB-E1-072": ("LIB", ["CON", "APP"]), "RWB-E1-042": ("LIB", ["CON", "APP", "OPS"]),
       "RWB-E1-043": ("LIB", ["CON", "APP"]), "RWB-E1-037": ("LIB", ["CON", "APP"]), "RWB-E1-047": ("LIB", ["CON", "APP"]),
       "RWB-E1-044": ("TPL", ["CON", "APP", "OPS"]), "RWB-E1-070": ("WF", ["CON", "APP"]), "RWB-E1-071": ("WF", ["CON", "APP"]),
       "RWB-E2-037": ("WF", ["CON", "APP"]), "RWB-E2-038": ("WF", ["CON", "APP"]), "RWB-E2-039": ("WF", ["CON", "APP"]),
       "RWB-E2-040": ("WF", ["CON", "APP"]), "RWB-E1-056": ("OBS", ["OPS"]),
       "NF-01": ("TPL", ["OPS"]), "NF-02": ("LIB", ["APP"]), "NF-03": ("TPL", ["OPS"]), "NF-04": ("TPL", ["OPS"]),
       "NF-05": ("TPL", ["OPS"]), "NF-06": ("DB", ["DB"]), "NF-07": ("EDGE", ["INF"]), "NF-08": ("WF", ["INF"])}
TE_DEFAULTED = {"RWB-TE-004", "RWB-TE-008", "RWB-TE-012"}
SVC_PART = {"RWB-E1-027": ("P7", ["CON", "APP"]), "RWB-E1-042": ("P3", ["CON"]), "RWB-E1-043": ("P3", ["CON"]),
            "RWB-E1-037": ("P4", ["CON", "APP"])}
SVC_FIXED = {"RWB-TE-013": "P10", "RWB-ACE-001": "P1"}
ITG_ONLY = {"RWB-TE-009", "RWB-TE-010"}
NEW = [("N001", "EDGE", "CON", "gateway-bff route contract", "TechX"),
       ("N001", "EDGE", "APP", "gateway-bff routes and composite screens", "TechX"),
       ("N002", "EVT", "INF", "Kafka topics, retry and dead-letter topics and ACLs", "INFRA"),
       ("N003", "WF", "INF", "Temporal namespace rwb-recovery and codec key", "INFRA"),
       ("N004", "TPL", "OPS", "Service pipeline template and Helm chart", "DEVOPS"),
       ("N005", "OBS", "OPS", "Platform dashboards and alerts baseline", "DEVOPS"),
       ("N006", "EDGE", "INF", "Redis session store for gateway-bff", "INFRA"),
       ("N007", "EDGE", "INF", "Partner gateway in the DMZ (FAPI 2.0)", "INFRA"),
       ("N008", "EVT", "INF", "Schema registry with BACKWARD compatibility", "INFRA"),
       ("N009", "LIB", "CON", "RFC 9457 problem and Idempotency-Key helpers - interface and fake", "TechX"),
       ("N009", "LIB", "APP", "RFC 9457 problem and Idempotency-Key helpers", "TechX"),
       ("N010", "WF", "CON", "Workflow kit templates - interface and fake", "TechX"),
       ("N010", "WF", "APP", "Workflow kit templates and codec server", "TechX"),
       ("N011", "DB", "DB", "PgBouncer pools, migrator role and grant check", "ACE"),
       ("N012", "EVT", "INF", "Blob, Key Vault and MFT/SFTP standard resources", "INFRA")]
NEW_ITG = [("W1J01", "W1", "Contract-test harness and synthetic test data"), ("W1J02", "W1", "Wave 1 v5 journey end to end"),
           ("W2J01", "W2", "Wave 2 journey end to end"), ("W3J01", "W3", "Wave 3 journey end to end"),
           ("W4J01", "W4", "Wave 4 journey end to end")]
I = re.I
MK = {"DP01": (r"\brecovery\.(?!v_ace_)\w+|recovery schema", I), "DP02": (r"recovery_svc", I),
      "DP03": (r"DecisionLogWriter|decision_log_entry|decision log", I), "DP04": (r"RuleEvaluator|RWB-E1-07[23]|Drools", I),
      "DP05": (r"AceSourceQuery|\bv_ace_|account_ext|party_ext", I), "DP06": (r"casewf\.config|\bparameters?\b|RWB-E1-042", I),
      "DP07": (r"reference data|\bLOV\b|RWB-E1-043", I), "DP08": (r"RecoveryAccessGuard|RWB-E1-037", I),
      "DP09": (r"application event|\bEV-\d+|outbox|RWB-TE-006", I), "DP10": (r"Quartz|\bJOB-\d+|RWB-TE-007", I),
      "DP11": (r"in-process|published interface", I), "DP12": (r"one workflow per case", I),
      "DP13": (r"/api/recovery/v1", I), "DP14": (r"rwb\.p\d+\.|rwb\.casewf\.", I), "DP15": (r"V0001 baseline|\bmigration\b", I),
      "DP16": (r"recovery\.integration\.adapter", I), "DP17": (r"data lake|INT-19|INT-20|lake_copy", I),
      "DP18": (r"interaction ledger", I), "DP19": (r"\bscreen|ace-web", I), "DP20": (r"agent client|RWB-TE-013", I)}
MKRX = {k: re.compile(p, f) for k, (p, f) in MK.items()}
BENIGN = {"DP01", "DP02", "DP06", "DP07", "DP08", "DP09", "DP13", "DP14", "DP15", "DP19"}
DP_DEPS = {"DP03": (["RWB-PLT-E1027-CON"], []), "DP04": (["RWB-PLT-E1072-CON"], ["RWB-P7-E1073-CON"]),
           "DP06": (["RWB-PLT-E1042-CON"], ["RWB-P3-E1042-CON"]), "DP07": (["RWB-PLT-E1043-CON"], ["RWB-P3-E1043-CON"]),
           "DP08": (["RWB-PLT-E1037-CON"], ["RWB-P4-E1037-CON"]), "DP09": (["RWB-PLT-TE006-CON"], []),
           "DP10": (["RWB-PLT-E1071-CON"], []), "DP14": (["RWB-PLT-E1047-CON"], []), "DP15": (["RWB-PLT-E1044-CON"], []),
           "DP16": ([], ["RWB-P2-E1007-CON"]), "DP19": (["RWB-PLT-N001-CON"], []), "DP20": ([], ["RWB-P10-TE013-CON"])}
CON_RX = re.compile(r"/api/recovery/v1/|\bEV-\d+\b|\b[A-Z][a-z]+(?:[A-Z][a-z]+)*Workflow\b|\bactivity\b|\bmanifest\b")
OPS_RX = re.compile(r"\bJOB-\d+|\balerts?\b|dashboard|run ?book|\bHelm\b|\bKEDA\b|\bsecrets?\b", I)
INF_RX = re.compile(r"\bBlob\b|Key Vault|private endpoint|\bMFT\b|\bSFTP\b|\bRedis\b")
DB_RX = re.compile(r"\bGRANT\b|\bdatabase login\b|PgBouncer|CREATE VIEW|create schema", I)
ITG_RX = re.compile(r"\bALS\b|\bBOT\b|SVAF|ACE Common|end[- ]to[- ]end|\bREC-\d+|Entra|\bpartner\b|\bemail\b|\bSMS\b|Nexus|\bMFT\b|\bledger\b|SCBPDM|\bEFS\b")
WRITE_RX = re.compile(r"\b(W|RW|CRU|CRUD|writes?|insert|update|creates?)\b", I)
EPIC_NAMES = {"RWB-PLT-TPL": "Service template and repositories", "RWB-PLT-LIB": "Shared libraries",
              "RWB-PLT-WF": "Temporal workflow platform", "RWB-PLT-DB": "ACE DB schemas and logins",
              "RWB-PLT-EVT": "Kafka event platform", "RWB-PLT-EDGE": "Edge and gateway", "RWB-PLT-OBS": "Observability",
              "RWB-ITG-W1": "Wave 1 integration", "RWB-ITG-W2": "Wave 2 integration", "RWB-ITG-W3": "Wave 3 integration",
              "RWB-ITG-W4": "Wave 4 integration", "RWB-ITG-NFR": "Non-functional integration"}
EPIC_NAMES.update({s["epic"]: f"{s['service']} ({s['name']})" for s in SERVICES})
OUT_DIR = "04 User stories/Recovery Workbench Service Story Files v1"

def ac_texts(block):
    parts = re.split(r"(?m)^\s*Scenario:\s*(AC\d+)\b", block); out = {}
    for i in range(1, len(parts), 2):
        out.setdefault(parts[i], re.split(r"(?m)^\s*(?:```|~~~|\| ID|### |\*\*)", parts[i + 1])[0])
    return out

def secondary(block, primary, tables):
    owners = []
    for line in block.splitlines():
        if not WRITE_RX.search(line):
            continue
        for t, o in tables.items():
            if o in SVC_CODES and o != primary and o not in owners and re.search(r"\b" + re.escape(t) + r"\b", line):
                owners.append(o)
    return owners

def lane_names(n):
    letters = string.ascii_uppercase
    return [letters[i] if i < 26 else letters[i // 26 - 1] + letters[i % 26] for i in range(n)]

def safe(s):
    return re.sub(r'[\\/:*?"<>|]+', " ", s).strip()[:110]

def build(index, blocks, own):
    tables = {t: v.get("owner") for t, v in (own.get("tables") or {}).items()}
    slices, legacy, asms, gaps = {}, {}, [], []
    A = lambda text, why, applied="": asms.append({"text": text, "why": why, "applied_in": applied})
    G = lambda title, desc, sev="P2", gtype="Missing", ref="": gaps.append({"title": title, "description": desc, "severity": sev, "type": gtype, "legacy_ref": ref})

    def add(scope, leg, wt, title, epic, n=None, **kw):
        sid = story_id(scope, leg, wt, n)
        if sid not in slices:
            d = dict(id=sid, scope=scope, legacy=leg, wt=wt, title=title, epic=epic, H=[], C=[], I=[], X=[], acs=[],
                     patterns=[], preserved=False, delta=False, secondary=False, new=False, owner=None)
            d.update(kw); slices[sid] = d
            legacy.setdefault(leg, {"disposition": "New", "slices": []})["slices"].append(sid)
        return sid

    def primary(r):
        k = r["key"]
        if k in ITG_ONLY: return "ITG"
        if k in SVC_FIXED: return SVC_FIXED[k]
        if k in SVC_PART: return SVC_PART[k][0]
        if k in PLT or r["group"] in ("TE", "NF"):
            return "PLT"
        if r.get("module"): return r["module"]
        d = {"AD": "P4", "DM": "P1"}.get(r["group"], "P3")
        A(f"{k} has no module code; primary service set to {d}", "Module field empty", k); return d

    for r in index:
        k, b = r["key"], blocks.get(r["key"], "")
        be = r.get("business_epic", "EP08"); wave = WMAP.get(be, 4)
        base = dict(business_epic=be, release=r.get("release", ""), build_status=BUILD_STATUS.get(k, "Not started"),
                    legacy_title=r["title"], source=r.get("story_file") or (f"04 User stories/{r['master']}" if r.get("master") else None),
                    reqs=r.get("reqs", []), tcs_legacy=r.get("tcs", []))
        if k in RETIRE_NEW:
            legacy[k] = {"disposition": "Retired (D-RCV-53)", "slices": []}; continue
        if k in ALREADY:
            legacy[k] = {"disposition": "Already retired", "slices": []}; continue
        pats = [p for p, rx in MKRX.items() if rx.search(b)]
        p = primary(r); acs = ac_texts(b)
        itg_acs = [a for a, t in acs.items() if ITG_RX.search(t)]
        app_acs = [a for a in acs if a not in itg_acs]
        sec = secondary(b, p, tables) if p in SVC_CODES else []
        if k in PRESERVED: disp = "Preserved + delta"
        elif k in MUST: disp = "Must change"
        elif k in NO_IMPACT: disp = "Moved (no impact)"
        elif not (set(pats) - BENIGN) and not sec and not itg_acs: disp = "Moved (no impact)"
        else: disp = "Split (rework)"
        legacy[k] = {"disposition": disp, "primary": p, "patterns": pats, "slices": [], "wave": wave}
        base["disposition"] = disp; base["patterns"] = pats; ttl = r["title"]
        if p == "ITG":
            add("ITG", k, "ITG", ttl, "RWB-ITG-NFR", wave=max(wave, 1), acs=list(acs), **base); continue
        if k in PLT:
            tag, wts = PLT[k]; e = f"RWB-PLT-{tag}"
            if k in TE_DEFAULTED:
                A(f"{k} placed in {e} (work type {wts[0]})", "no service owner stated in the legacy story", k)
            if disp == "Preserved + delta" and k not in SVC_PART:
                add("PLT", k, "APP", ttl, e, wave=0, preserved=True, acs=list(acs), **base)
                for wt in wts:
                    add("PLT", k, wt, ttl, e, n=(2 if wt == "APP" else None), wave=0, delta=True, **base)
            else:
                for wt in wts:
                    add("PLT", k, wt, ttl, e, wave=0, acs=(list(acs) if (wt == "APP" and k not in SVC_PART) else []),
                        delta=(disp == "Preserved + delta"), **base)
            if k in SVC_PART:
                sc, swts = SVC_PART[k]; se = svc(sc)["epic"]
                if disp == "Preserved + delta":
                    add(sc, k, "APP", ttl, se, wave=wave, preserved=True, acs=list(acs), **base)
                for wt in swts:
                    add(sc, k, wt, ttl, se, wave=wave, acs=(app_acs if wt == "APP" else []), delta=(disp == "Preserved + delta"), **base)
                if disp != "Preserved + delta":
                    add("ITG", k, "ITG", ttl, f"RWB-ITG-W{max(wave, 1)}", wave=max(wave, 1), acs=itg_acs, **base)
            continue
        se = svc(p)["epic"]
        if k == "RWB-ACE-001":
            add(p, k, "DB", ttl, se, wave=wave, acs=list(acs), **base); continue
        if disp == "Moved (no impact)":
            if k not in NO_IMPACT and CON_RX.search(b):
                add(p, k, "CON", ttl, se, wave=wave, **base)
            add(p, k, "APP", ttl, se, wave=wave, acs=list(acs), **base); continue
        if CON_RX.search(b): add(p, k, "CON", ttl, se, wave=wave, **base)
        add(p, k, "APP", ttl, se, wave=wave, acs=app_acs, **base)
        for s2 in sec:
            add(s2, k, "APP", ttl, svc(s2)["epic"], wave=wave, secondary=True, **base)
        if DB_RX.search(b): add(p, k, "DB", ttl, se, wave=wave, **base)
        if INF_RX.search(b): add(p, k, "INF", ttl, se, wave=wave, **base)
        if OPS_RX.search(b): add(p, k, "OPS", ttl, se, wave=wave, **base)
        if itg_acs or sec:
            add("ITG", k, "ITG", ttl, f"RWB-ITG-W{max(wave, 1)}", wave=max(wave, 1), acs=itg_acs, **base)

    nb = dict(business_epic="NEW", release="", build_status="Not started", legacy_title="", source=None, reqs=[],
              tcs_legacy=[], disposition="New", patterns=[])
    for key, tag, wt, ttl, owner in NEW:
        add("PLT", key, wt, ttl, f"RWB-PLT-{tag}", wave=0, new=True, owner=owner, **nb)
    for key, w, ttl in NEW_ITG:
        add("ITG", key, "ITG", ttl, f"RWB-ITG-{w}", wave=int(w[1]), new=True, owner="QA", **nb)
    nseq = 13
    for s in SERVICES:
        if not any(x["scope"] == s["code"] and x["wt"] == "CON" for x in slices.values()):
            add(s["code"], f"N{nseq:03d}", "CON", f"{s['service']} service contract baseline", s["epic"], wave=s["wave"], new=True, **nb)
            A(f"{s['service']} had no contract-bearing legacy story; contract baseline N{nseq:03d} created", "Day-1 rule R5.7", s["epic"]); nseq += 1

    by_leg = {}
    for x in slices.values():
        by_leg.setdefault(x["legacy"], []).append(x["id"])
    def find(scope, leg, wt, n=None):
        sid = f"RWB-{scope}-{leg_compact(leg)}-{wt}" + (f"-{n}" if n else "")
        return sid if sid in slices else None
    def main_app(leg):
        p = legacy.get(leg, {}).get("primary")
        return find(p, leg, "APP") if p else None
    def itg_of(leg):
        hit = [i for i in by_leg.get(leg, []) if slices[i]["wt"] == "ITG"]
        if hit: return hit[0]
        src = slices[main_app(leg)] if main_app(leg) else None
        w = max(1, legacy[leg].get("wave", 1))
        keep = {k: src[k] for k in ("business_epic", "release", "build_status", "legacy_title", "source", "reqs", "tcs_legacy", "disposition", "patterns")} if src else nb
        sid = add("ITG", leg, "ITG", slices[by_leg[leg][0]]["title"], f"RWB-ITG-W{w}", wave=w, **keep)
        by_leg[leg].append(sid); return sid
    def push(lst, v):
        if v and v not in lst: lst.append(v)

    for r in index:
        k = r["key"]; lg = legacy.get(k, {})
        if lg.get("disposition") in ("Retired (D-RCV-53)", "Already retired"): continue
        a_id = main_app(k)
        if not a_id: continue
        a = slices[a_id]; pa = lg["primary"]
        push(a["H"], find(pa, k, "CON"))
        for wt in ("DB", "INF", "OPS"):
            push(a["X"], find(pa, k, wt))
        for dp in lg.get("patterns", []):
            hs, cs = DP_DEPS.get(dp, ([], []))
            for h in hs:
                if h in slices and h != a_id: push(a["H"], h)
            for c in cs:
                if c in slices and slices[c]["scope"] != pa: push(a["C"], c)
                elif c in slices: push(a["H"], c)
        for sid in by_leg.get(k, []):
            s2 = slices[sid]
            if s2["secondary"]:
                push(s2["C"], find(pa, k, "CON"))
        for B in r.get("deps", []):
            if B == "RWB-E1-014": continue
            if B == "RWB-TE-007":
                push(a["H"], "RWB-PLT-E1071-CON" if "RWB-PLT-E1071-CON" in slices else None); continue
            if B in ALREADY:
                A(f"{k} depended on already retired {B}; dependency dropped", "legacy dependency on a cancelled story", k); continue
            if B not in legacy:
                G(f"{k} depends on unknown {B}", f"{B} is not in any story master", "P3", "Missing", k); continue
            if B in PLT:
                push(a["H"], find("PLT", B, "CON")) if find("PLT", B, "CON") else push(a["X"], by_leg[B][0])
                if B in SVC_PART:
                    sc = SVC_PART[B][0]; c = find(sc, B, "CON")
                    if c and sc != pa: push(a["C"], c)
                    elif c: push(a["H"], c)
                continue
            pb = legacy[B].get("primary")
            if pb == pa:
                push(a["H"], main_app(B) or by_leg[B][0]); continue
            c = find(pb, B, "CON") if pb in SVC_CODES else None
            if c: push(a["C"], c)
            tgt = main_app(B) or by_leg[B][0]
            push(slices[itg_of(k)]["I"], tgt)
        for sid in by_leg.get(k, []):
            if slices[sid]["wt"] == "ITG":
                for o in by_leg[k]:
                    if slices[o]["wt"] == "APP": push(slices[sid]["I"], o)
    for x in slices.values():
        x["H"] = [h for h in x["H"] if h != x["id"]]
        if x["wt"] == "CON":
            x["H"] = []

    g = nx.DiGraph()
    for x in slices.values():
        if x["wt"] != "CON": g.add_node(x["id"])
    for x in slices.values():
        for h in x["H"]:
            if h in slices and slices[h]["wt"] != "CON": g.add_edge(h, x["id"])

    def con_for(u):
        s = slices[u]; cid = find(s["scope"], s["legacy"], "CON")
        if not cid:
            keep = {k: s[k] for k in ("business_epic", "release", "build_status", "legacy_title", "source", "reqs", "tcs_legacy", "disposition", "patterns")}
            cid = add(s["scope"], s["legacy"], "CON", s["title"], s["epic"], wave=s["wave"], lane_split=True, **keep)
            by_leg.setdefault(s["legacy"], []).append(cid)
        return cid

    def cut(u, v, why):
        g.remove_edge(u, v); slices[v]["H"].remove(u); c = con_for(u)
        if c not in slices[v]["H"]: slices[v]["H"].append(c)
        A(f"{v} builds against {c} (contract and fake) instead of waiting for {u}", why, v)

    while True:
        try:
            cyc = nx.find_cycle(g)
        except nx.NetworkXNoCycle:
            break
        u, v = cyc[-1][0], cyc[-1][1]; cut(u, v, "dependency cycle")
    changed = True
    while changed:
        changed = False
        for comp in list(nx.weakly_connected_components(g)):
            path = nx.dag_longest_path(g.subgraph(comp))
            if len(path) > 4:
                cut(path[3], path[4], "lane depth above 4 (R5.7 rule 5)"); changed = True; break

    for epic in sorted({x["epic"] for x in slices.values()}):
        nodes = [x["id"] for x in slices.values() if x["epic"] == epic and x["wt"] != "CON"]
        comps = sorted((sorted(c) for c in nx.weakly_connected_components(g.subgraph(nodes))), key=lambda c: min(slices[i]["legacy"] for i in c))
        code = epic.replace("RWB-SVC-", "").replace("RWB-", "")
        for name, comp in zip(lane_names(len(comps)), comps):
            for i in comp:
                slices[i]["lane"] = (f"L-{code}" if epic.startswith("RWB-ITG") else f"L-{code}-{name}")
    for x in slices.values():
        if x["wt"] == "CON":
            x["lane"] = f"CG-W{x['wave']}"
        if not x["owner"]:
            x["owner"] = "QA" if x["epic"] == "RWB-ITG-NFR" else WT_OWNER[x["wt"]]
        non_con = [h for h in x["H"] if slices[h]["wt"] != "CON"]
        x["ready"] = "Day 1" if x["wt"] == "CON" or not non_con else "After " + ", ".join(non_con)
        n = x["id"].rsplit("-", 1)[-1] if re.search(r"-[2-9]$", x["id"]) else ""
        fname = f"RWB {x['scope']} {leg_compact(x['legacy'])} {x['wt']}{('-' + n) if n else ''} {safe(x['title'])}{WT_SUFFIX[x['wt']]} v1.md"
        x["file"] = f"{OUT_DIR}/{x['epic']} {EPIC_NAMES[x['epic']]}/{fname}"
        x["service"] = svc(x["scope"])["service"] if x["scope"] in SVC_CODES else ("platform" if x["scope"] == "PLT" else "integration")
    seen = set()
    for x in slices.values():
        if x["scope"] in SVC_CODES and 0 < x["wave"] < svc(x["scope"])["wave"] and (x["scope"], x["business_epic"]) not in seen:
            seen.add((x["scope"], x["business_epic"]))
            G(f"Wave conflict {x['scope']} / {x['business_epic']}",
              f"{x['business_epic']} stories are wave {x['wave']} by W-MAP but {svc(x['scope'])['service']} is wave {svc(x['scope'])['wave']} in Arch v5; W-MAP kept",
              "P2", "Conflict", x["legacy"])
    for k, lg in legacy.items():
        lg["slices"] = [i for i in by_leg.get(k, [])] if lg.get("slices") is not None else []
    teams = sorted({x["owner"] for x in slices.values() if x["ready"] == "Day 1"})
    stats = {"slices": len(slices), "legacy": len(legacy), "day1": sum(1 for x in slices.values() if x["ready"] == "Day 1"),
             "day1_teams": teams, "lanes": len({x["lane"] for x in slices.values()})}
    return {"slices": sorted(slices.values(), key=lambda x: x["id"]), "legacy": legacy, "stats": stats, "asms": asms, "gaps": gaps}

def load_blocks(index):
    import legacy_index as li
    blocks = {}
    for m in sorted({r["master"] for r in index if r.get("master")}):
        text = (STORIES / m).read_text(encoding="utf-8")
        heads = list(li.HEAD.finditer(text))
        for i, h in enumerate(heads):
            blocks.setdefault(h.group(1), text[h.start(): heads[i + 1].start() if i + 1 < len(heads) else len(text)])
    for r in index:
        if r.get("story_file"):
            blocks[r["key"]] = (ROOT / r["story_file"]).read_text(encoding="utf-8")
    return blocks

def main():
    index = read_json(WORK / "plan" / "legacy_index.json")
    own = read_json(WORK / "plan" / "ownership.json", {})
    plan = build(index, load_blocks(index), own)
    reset_cands("A7")
    for a in plan.pop("asms"):
        add_asm("A7", a["text"], a["why"], read="split_plan.py rules (Appendix R5-R6)", applied_in=a["applied_in"], confidence="Medium")
    for gp in plan.pop("gaps"):
        add_gap("A7", gp["title"], gp["description"], gtype=gp["type"], severity=gp["severity"], legacy_ref=gp["legacy_ref"],
                source="04 User stories masters", area="Story realignment")
    write_json(WORK / "plan" / "split_plan.json", plan)
    print("A7a OK", plan["stats"])

if __name__ == "__main__":
    main()
```

- [ ] **Step 4: Run the tests, then the split.**

```powershell
python -I "22 Microservice Realignment/compat/split_plan.py"
```

Expected: tests OK, then a line like `A7a OK {'slices': <900–1300>, 'legacy': <about 370>, 'day1': <n>, 'day1_teams': ['ACE', 'DEVOPS', 'INFRA', 'QA', 'TechX'], 'lanes': <n>}`.

If `day1_teams` is missing a team, check the `NEW` list in `split_plan.py`. Never edit `split_plan.json` by hand.

---

### Task 13: Office writer and work-package generator (step A7b)

**Files:**
- Create: `22 Microservice Realignment/compat/office_write.py`
- Create: `22 Microservice Realignment/compat/make_wps.py`
- Test: `22 Microservice Realignment/compat/tests/test_office_write.py`, `22 Microservice Realignment/compat/tests/test_make_wps.py`
- Output:
  - `_work/msr/wp/*.md`
  - `_work/msr/wp/queue-{A10,B,C,D}.json`
  - `_work/msr/plan/docs.json`, the document-family list that the Tracker uses

- [ ] **Step 1: Write the failing tests.**

```python
# tests/test_office_write.py
import json, tempfile, unittest
from pathlib import Path
import docx, openpyxl
from pptx import Presentation
import office_write as ow

class TestOffice(unittest.TestCase):
    def test_md_docx_xlsx_pptx(self):
        with tempfile.TemporaryDirectory() as d:
            d = Path(d); md = d / "a.md"
            md.write_text("# Title\n\nPara one.\n\n- item\n\n| ID | Text |\n|---|---|\n| BR-1 | One |\n", encoding="utf-8")
            ow.md_docx(md, d / "a.docx")
            doc = docx.Document(d / "a.docx")
            self.assertEqual(doc.paragraphs[0].text, "Title"); self.assertEqual(doc.tables[0].cell(1, 0).text, "BR-1")
            wb = openpyxl.Workbook(); wb.active.title = "Log"; wb.save(d / "x.xlsx")
            (d / "rows.json").write_text(json.dumps([["ID", "Decision"], ["D-RCV-53", "Realign"]]))
            ow.xlsx_append(d / "x.xlsx", "New", d / "rows.json")
            self.assertEqual(openpyxl.load_workbook(d / "x.xlsx")["New"]["A2"].value, "D-RCV-53")
            Presentation().save(d / "p.pptx"); (d / "s.md").write_text("## Slide A\n- one\n- two\n", encoding="utf-8")
            ow.pptx_append(d / "p.pptx", d / "s.md")
            self.assertEqual(len(Presentation(d / "p.pptx").slides), 1)
            with self.assertRaises(SystemExit):
                ow.copy(d / "a.docx", d / "a.docx")
```

```python
# tests/test_make_wps.py
import unittest
import make_wps as mw

class TestWps(unittest.TestCase):
    def test_chunks_and_text(self):
        slices = [{"id": f"RWB-P3-E1{n:03d}-APP", "legacy": f"RWB-E1-{n:03d}", "epic": "RWB-SVC-P3", "lane": "L-P3-A",
                   "wt": "APP", "file": f"04/x{n}.md", "scope": "P3", "source": "04 User stories/m.md"} for n in range(1, 12)]
        wps = mw.story_wps({"slices": slices}, fanout=5)
        self.assertEqual(len(wps), 3)
        self.assertTrue(all(len(w["keys"]) <= 5 for w in wps))
        self.assertIn("fanout: 5", wps[0]["text"]); self.assertIn("04/x1.md", wps[0]["text"])
        self.assertIn("_work/msr/fragments/RWB-P3-E1001-APP.json", wps[0]["expect"])
        self.assertTrue(wps[0]["wp"].startswith("B-P3-"))
```

- [ ] **Step 2: Run the tests.** Expected: FAIL (import errors).

- [ ] **Step 3: Write `office_write.py`.**

```python
"""Office helpers for agents (replace the Anthropic docx/xlsx/pptx skills). Never overwrites an existing file."""
import argparse, json, re, shutil, sys
from pathlib import Path

def _guard(dst):
    if Path(dst).exists():
        raise SystemExit(f"REFUSED: {dst} exists (never edit an existing file; use the next version)")

def copy(src, dst):
    _guard(dst); src = Path(src)
    shutil.copytree(src, dst) if src.is_dir() else shutil.copy2(src, dst)
    print("COPIED", src, "->", dst)

def _rows(block):
    rows = [[c.strip().replace("\\|", "|") for c in re.split(r"(?<!\\)\|", l.strip().strip("|"))] for l in block]
    return [r for r in rows if not all(set(c) <= set("-: ") for c in r)]

def md_docx(md, out, template=None):
    import docx
    _guard(out)
    doc = docx.Document(template) if template else docx.Document()
    if template:
        body = doc.element.body
        for el in list(body):
            if not el.tag.endswith("sectPr"):
                body.remove(el)
    lines = Path(md).read_text(encoding="utf-8").splitlines(); i = 0
    while i < len(lines):
        l = lines[i]
        if l.startswith("|"):
            blk = []
            while i < len(lines) and lines[i].startswith("|"):
                blk.append(lines[i]); i += 1
            rows = _rows(blk)
            if rows:
                w = max(len(r) for r in rows); t = doc.add_table(rows=len(rows), cols=w)
                try:
                    t.style = "Table Grid"
                except Exception:
                    pass
                for r, row in enumerate(rows):
                    for c in range(w):
                        t.cell(r, c).text = row[c] if c < len(row) else ""
            continue
        m = re.match(r"^(#{1,6})\s+(.*)$", l)
        if m:
            doc.add_heading(m.group(2).strip(), min(len(m.group(1)), 4))
        elif re.match(r"^\s*[-*]\s+", l):
            try:
                doc.add_paragraph(re.sub(r"^\s*[-*]\s+", "", l), style="List Bullet")
            except KeyError:
                doc.add_paragraph("• " + re.sub(r"^\s*[-*]\s+", "", l))
        elif l.strip():
            doc.add_paragraph(l.replace("**", ""))
        i += 1
    doc.save(out); print("WROTE", out)

def xlsx_append(xlsx, sheet, rows_json):
    import openpyxl
    wb = openpyxl.load_workbook(xlsx); rows = json.loads(Path(rows_json).read_text(encoding="utf-8"))
    ws = wb[sheet] if sheet in wb.sheetnames else wb.create_sheet(sheet[:31])
    for r in rows:
        ws.append(r)
    wb.save(xlsx); print("APPENDED", len(rows), "rows to", sheet)

def md_xlsx(md, out):
    from xlsx_write import write_book
    _guard(out); sheets, name, blk = {}, "Sheet", []
    def flush():
        rows = _rows(blk)
        if rows:
            sheets[name[:31] if name not in sheets else (name[:28] + str(len(sheets)))] = (rows[0], rows[1:])
    for l in Path(md).read_text(encoding="utf-8").splitlines() + [""]:
        if l.startswith("|"):
            blk.append(l); continue
        if blk:
            flush(); blk = []
        m = re.match(r"^#{1,6}\s+(.*)$", l)
        if m:
            name = re.sub(r"[\[\]:*?/\\]", " ", m.group(1)).strip() or "Sheet"
    write_book(out, sheets); print("WROTE", out)

def pptx_append(pptx, slides_md):
    from pptx import Presentation
    prs = Presentation(pptx); cur = None
    layout = prs.slide_layouts[1] if len(prs.slide_layouts) > 1 else prs.slide_layouts[0]
    for l in Path(slides_md).read_text(encoding="utf-8").splitlines():
        if l.startswith("## "):
            cur = prs.slides.add_slide(layout); cur.shapes.title.text = l[3:].strip()
            body = [s for s in cur.placeholders if s.placeholder_format.idx == 1]
            cur._body = body[0].text_frame if body else None; cur._first = True
        elif cur is not None and l.strip() and cur._body is not None:
            txt = re.sub(r"^\s*[-*]\s+", "", l)
            if cur._first:
                cur._body.text = txt; cur._first = False
            else:
                cur._body.add_paragraph().text = txt
    prs.save(pptx); print("APPENDED slides to", pptx)

if __name__ == "__main__":
    sys.path.insert(0, str(Path(__file__).resolve().parent))
    ap = argparse.ArgumentParser(); sub = ap.add_subparsers(dest="cmd", required=True)
    a = sub.add_parser("copy"); a.add_argument("src"); a.add_argument("dst")
    a = sub.add_parser("md-docx"); a.add_argument("md"); a.add_argument("out"); a.add_argument("--template")
    a = sub.add_parser("md-xlsx"); a.add_argument("md"); a.add_argument("out")
    a = sub.add_parser("xlsx-append"); a.add_argument("xlsx"); a.add_argument("sheet"); a.add_argument("rows_json")
    a = sub.add_parser("pptx-append"); a.add_argument("pptx"); a.add_argument("slides_md")
    x = ap.parse_args()
    {"copy": lambda: copy(x.src, x.dst), "md-docx": lambda: md_docx(x.md, x.out, x.template),
     "md-xlsx": lambda: md_xlsx(x.md, x.out), "xlsx-append": lambda: xlsx_append(x.xlsx, x.sheet, x.rows_json),
     "pptx-append": lambda: pptx_append(x.pptx, x.slides_md)}[x.cmd]()
```

- [ ] **Step 4: Write `make_wps.py`.**

```python
"""Write every WP file and the queues. All WPs in a queue are independent (single-writer rule)."""
import json, sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
from common import ROOT, WORK, SERVICES, STORIES, latest_path, versions, next_version, read_json, write_json, svc

TPL = "22 Microservice Realignment/Recovery Workbench Microservice Story Template and Rules v1.md"
OFFICE = "22 Microservice Realignment/compat/office_write.py"
CONVERT = "22 Microservice Realignment/compat/convert_sources.py"
V5 = "22 Microservice Realignment/Recovery Workbench Architecture v5 Text Extract v1.md"
TD = "22 Microservice Realignment/Recovery Workbench Temporal and Drools Design Text Extract v1.md"
OWN = "_work/msr/plan/ownership.json"
HEADER = "Tool rules: AGENTS.md (root) rules 1-14. Agent: {agent}. fanout: {fanout}\n"
FINISH = ("Finish: run python -I \"22 Microservice Realignment/checks/run_all.py\" --wp {wp} --quick ; fix every failure ; "
          "write _work/msr/editlog/{wp}.md (files written, tool line T3 Code / OpenCode / DeepSeek v4.1 Flash, counts of CG and ASM rows) ; "
          "reply with the list of files written.\n")
KEEP = ("id", "title", "wt", "epic", "service", "lane", "ready", "owner", "wave", "business_epic", "release", "legacy",
        "disposition", "build_status", "patterns", "H", "C", "I", "X", "acs", "tcs_legacy", "reqs", "preserved", "delta",
        "secondary", "new", "file", "source")

STORY_RULES = """Do, for each story line below (one JSON object per line), write exactly one file at its "file" path:
1. Use the template in Template and Rules v1 §R7: the 19 headings in order, the metadata table rows of §R7.1 in order (never remove a row).
   Copy these values exactly from the JSON: Story key=id, Work type, Suggested owner (fixed phrase for "owner"), Service, Service epic=epic,
   Wave, Business epic, Release (+ " (tentative)"; "None (new story)" when empty), Legacy key, Legacy disposition, Build status,
   Patterns applied, Parallel lane, Ready to start, Depends on (build)=H, Contract dependencies=C, Integration dependencies=I,
   External dependencies=X, PRD reference "Pending (C1)", Status "Draft (realignment v1)".
2. preserved=true: copy legacy §1-11, §14-16, §18 and §19 word for word; keep §12 and §13 under the heading "As built (monolith)".
3. delta=true: describe only the microservice change for that legacy key in Template and Rules §R6.
4. ACs: "acs" lists the legacy AC IDs this story owns. Copy each verbatim with the origin tag "(legacy <legacy> <AC>)".
   An APP AC whose cross-service part can be mocked gets the Given "Given the <service> contract mock returns <x>" (keep every value).
   CON, DB, INF, OPS and new stories: write ACs tagged "(new, D-RCV-53)" that test only the deliverable in the title. Never invent business values.
5. TCs: keep the legacy TC IDs of the ACs this story owns; an ITG copy of a TC gets the suffix -ITG. Add the Level column (§R7.2 s16).
6. Apply the DP table (§R5.5) for every pattern in "patterns"; list them in "Patterns applied".
7. Section 12 Contract: tables 12.1-12.9 (or None). Names: topic rwb.<short>.events.v1, event rwb.<short>.<Event>.v1, queue rwb-<short>,
   REST base /api/recovery/<short>/v1, schema rwb_<name>. Owners come from the Ownership Map only.
8. Write _work/msr/fragments/<id>.json with keys: id, epic, service, wt, lane, ready, owner, business_epic, wave, release, legacy,
   disposition, H, C, I, X, acs [{"id","origin","text_first_line"}], tcs, reqs, ops_provided, ops_consumed, events_published,
   events_consumed, workflows, prd_ref "Pending (C1)", gaps [CG ids], assumptions [ASM ids], file.
9. A missing value: "Not specified in the source documents (CG-{wp}-<n>; ASM-{wp}-<n>)" plus one combined gap row per story and one
   assumption row per default (formats in Template and Rules §R9) in _work/msr/gaps/{wp}.jsonl and _work/msr/assumptions/{wp}.jsonl.
"""

def _src_lines(sl):
    out = []
    for s in sl:
        src = s.get("source")
        if src and f"- {src} (heading {s['legacy']})" not in out:
            out.append(f"- {src} (heading {s['legacy']})")
    return out

def story_wps(plan, fanout=5):
    groups = {}
    for s in plan["slices"]:
        groups.setdefault(s["epic"], {}).setdefault(s["legacy"], []).append(s)
    wps = []
    for epic, by_leg in sorted(groups.items()):
        keys = sorted(by_leg, key=lambda k: (min(x.get("lane", "") for x in by_leg[k]), k))
        code = epic.replace("RWB-SVC-", "").replace("RWB-", "")
        for n in range(0, len(keys), 5):
            chunk = keys[n:n + 5]; sl = [s for k in chunk for s in by_leg[k]]
            wp = f"B-{code}-{n // 5 + 1:02d}"
            mod = sl[0].get("scope") if sl[0].get("scope") not in ("PLT", "ITG") else None
            reads = [f"- {TPL} (read fully first)", f"- {OWN}", f"- {V5}", f"- {TD}"] + _src_lines(sl)
            if mod:
                reads.append(f"- _work/msr/extract/ files of the FSD and TSD folders whose name contains \"{mod}\" (module {svc(mod)['name']})")
            reads.append("- Thin stories only: _work/msr/extract/Recovery Workbench Business Requirements Program v4.md, Epic 1 v4, Epic 2 v2, "
                         "Epics 3 to 8 Specification v3, Business Rules and Routing Logic (fill order Template and Rules §R7.3)")
            outs = [s["file"] for s in sl] + [f"_work/msr/fragments/{s['id']}.json" for s in sl]
            f = len(chunk) > 1
            text = (f"# WP {wp} — {epic}: legacy {', '.join(chunk)}\n" + HEADER.format(agent="aisdlc-msr-worker", fanout=fanout if f else 0)
                    + "Read only:\n" + "\n".join(reads) + "\nWrite only:\n" + "\n".join(f"- {o}" for o in outs)
                    + f"\n- _work/msr/gaps/{wp}.jsonl\n- _work/msr/assumptions/{wp}.jsonl\n- _work/msr/editlog/{wp}.md\n"
                    + STORY_RULES.replace("{wp}", wp) + "Stories:\n"
                    + "\n".join(json.dumps({k: s.get(k) for k in KEEP}, ensure_ascii=False) for s in sl) + "\n"
                    + (f"Parallel: give each legacy key to its own task subagent (aisdlc-msr-worker) in ONE message, up to {fanout} at once; "
                       "each subagent writes only that key's files and its own jsonl rows with ids CG-" + wp + "-<key>-<n>.\n" if f else "")
                    + FINISH.format(wp=wp))
            wps.append({"wp": wp, "keys": chunk, "text": text, "expect": outs + [f"_work/msr/editlog/{wp}.md"], "fanout": f,
                        "agent": "aisdlc-msr-worker"})
    return wps

DOCS = [  # track, folder, family stem, what changes (Appendix R8.6)
    ("TECH", "05 Technical architecture", "Recovery Workbench ACE Architecture Decision", "19 services inside ACE; supersedes the single-service decision"),
    ("TECH", "05 Technical architecture", "Recovery Workbench Target Architecture", "v5 target: 19 services, Kafka, Temporal layer, edge, no data lake"),
    ("TECH", "05 Technical architecture", "Recovery Workbench Technical Specifications by Module", "add a T0 Service section per module; rewrite T5.2 as contracts"),
    ("TECH", "05 Technical architecture", "Recovery Workbench Interface Specifications", "remove INT-19 and INT-20 (no data lake); per-service owners"),
    ("TECH", "05 Technical architecture", "Recovery Workbench Environment and Deployment Design", "per-service deployments; environment names are a gap"),
    ("TECH", "05 Technical architecture", "Recovery Workbench Workflow Engine Design", "workflow kit, child workflow per stage, Schedules"),
    ("TECH", "05 Technical architecture", "Recovery Workbench Rules Engine Design", "embedded Drools per service; registry in rwb-decision"),
    ("TECH", "05 Technical architecture", "Recovery Workbench Security and Access Design", "login per service, workload identity, authorise contract"),
    ("TECH", "05 Technical architecture", "Recovery Workbench Observability and Monitoring Design", "per-service dashboards and alerts"),
    ("TECH", "05 Technical architecture", "Recovery Workbench Error Handling and Resilience Standard", "2 s timeout, one REST hop, retry and .dlt rules"),
    ("TECH", "05 Technical architecture", "Recovery Workbench Availability Performance and Recovery Design", "per-service targets; RPO and RTO are a gap"),
    ("TECH", "05 Technical architecture", "Recovery Workbench Audit and Logging Design", "local decision record plus central ledger"),
    ("TECH", "05 Technical architecture", "Recovery Workbench Document Management Design", "owned by rwb-document"),
    ("TECH", "05 Technical architecture", "Recovery Workbench Notification and Correspondence Design", "owned by rwb-comms"),
    ("TECH", "05 Technical architecture", "Recovery Workbench Information Flow", "flows between the 19 services"),
    ("TECH", "05 Technical architecture", "Recovery Workbench System Disposition and Integration Inventory", "add Service column"),
    ("DATA", "06 Data", "Recovery Workbench Conceptual Data Model", "add owning service per entity"),
    ("DATA", "06 Data", "Recovery Workbench Source to Target Mapping", "target schema rwb_<name>"),
    ("DATA", "06 Data", "Recovery Workbench Reference Data and Lists of Values", "refdata starter; shared lists via rwb-case"),
    ("DATA", "06 Data", "Recovery Workbench Data Ownership and Stewardship", "owner service per data set"),
    ("DATA", "06 Data", "Recovery Workbench Data Migration Approach", "migration per schema"),
    ("DATA", "06 Data", "Recovery Workbench Party and Customer Master Data Design", "read only through rwb-source-data"),
    ("DATA", "06 Data", "Recovery Workbench Reporting and Analytics Data Model", "no data lake; rwb-reporting read model from events"),
    ("DATA", "06 Data", "Recovery Workbench Data Classification and Personal Data Inventory", "no PII in events, workflow inputs or logs"),
    ("DATA", "06 Data", "Recovery Workbench Data Quality and Reconciliation Rules", "per-service reconciliation"),
    ("DATA", "06 Data", "Recovery Workbench Volume and Scale Forecast", "per-service volumes, topics and queues"),
    ("REQ-SPEC", "03 Requirements and specifications", "Recovery Workbench Functional Specifications by Module", "add only a Service line and a v5 note per module"),
    ("REQ-SPEC", "03 Requirements and specifications", "Recovery Workbench Non Functional Specification", "2 s timeout, one-hop REST; gaps for RPO/RTO and 'weeks vs 28 days'"),
    ("AI", "08 AI and agents", "Recovery Workbench AI and Agent Architecture", "rwb-agent service; AgentRunWorkflow child, 60 s fallback"),
    ("AI", "08 AI and agents", "Recovery Workbench Model Integration Design", "model calls only from rwb-agent activities"),
    ("AI", "08 AI and agents", "Recovery Workbench Agent Catalog and Specifications", "owning service per agent"),
    ("CTRL", "10 Policy, controls and compliance", "Recovery Workbench Controls Catalog", "control owner service"),
    ("CTRL", "10 Policy, controls and compliance", "Recovery Workbench Records Retention and Archiving", "retention per schema"),
    ("CTRL", "10 Policy, controls and compliance", "Recovery Workbench Personal Data Protection Design", "PII boundaries per service and in events"),
    ("CTRL", "10 Policy, controls and compliance", "Recovery Workbench Regulatory Requirements Map", "regulation to service"),
    ("BIZ", "02 Business architecture and process", "Recovery Workbench Feature List", "add Service and Service epic columns"),
    ("BIZ", "02 Business architecture and process", "Recovery Workbench Case and Workflow Model", "CaseWorkflow parent with child per stage"),
    ("BIZ", "02 Business architecture and process", "Recovery Workbench Users Roles and Permissions", "authorise contract of rwb-access"),
    ("TESTDOC", "09 Testing and quality", "Recovery Workbench Test Strategy", "contract tests, component tests with mocks, ITG per wave"),
    ("TESTDOC", "09 Testing and quality", "Recovery Workbench Non Functional Test Plan", "per-service and journey NFR tests"),
    ("TESTDOC", "09 Testing and quality", "Recovery Workbench Test Data Plan", "synthetic data per schema; contract mocks"),
    ("TESTDOC", "09 Testing and quality", "Recovery Workbench Definition of Ready and Done", "Ready = contract published; Done = contract and boundary tests green"),
    ("TESTDOC", "09 Testing and quality", "Recovery Workbench Integration Test Plan", "NEW v1: ITG-W1..W4 and NFR epics, harness RWB-ITG-W1J01-ITG"),
    ("DELIVDOC", "11 Delivery and operations", "Recovery Workbench Engineering Practices", "repo per service, contract-first, per-service Flyway"),
    ("DELIVDOC", "11 Delivery and operations", "Recovery Workbench Release Plan", "waves within the 8-month horizon; dates unchanged and tentative"),
    ("DELIVDOC", "11 Delivery and operations", "Recovery Workbench Cutover and Go Live Plan", "cutover per wave"),
    ("DELIVDOC", "11 Delivery and operations", "Recovery Workbench Run Operating Model", "run book per service"),
    ("DELIVDOC", "11 Delivery and operations", "Recovery Workbench Risks Assumptions Issues and Dependencies", "add realignment risks R1-R9; point to the Assumptions Register"),
    ("DELIVDOC", "11 Delivery and operations", "Recovery Workbench Resource Plan and Team Structure", "suggested ownership by team type; no names"),
]
ARCH = [  # wp, title, sources (folder, stem), outputs (folder, stem, ext or 'dir' or 'new:<name>'), note
    ("B-ARCH-ADR", "ADR v-next with ADR-013..023", [("05 Technical architecture", "Recovery Workbench Architecture Decision Records")],
     [("05 Technical architecture", "Recovery Workbench Architecture Decision Records", ".md")], "Appendix R §R8.4 row ADR"),
    ("B-ARCH-DL", "Decision Log v-next", [("01 Decisions and governance", "Recovery Workbench Decision Log")],
     [("01 Decisions and governance", "Recovery Workbench Decision Log", ".xlsx")], "add D-RCV-53 and DL44-49; mark D-RCV-36 T1 and T2 amended"),
    ("B-ARCH-SVC", "Service Catalog v1 and Service Template Specification v1", [],
     [("05 Technical architecture", "Recovery Workbench Service Catalog", ".md"), ("05 Technical architecture", "Recovery Workbench Service Catalog", ".xlsx"),
      ("05 Technical architecture", "Recovery Workbench Service Template Specification", ".md")], "19 services, resources per service, template"),
    ("B-ARCH-API", "API Specification folder v-next split into 19 files", [("05 Technical architecture", "Recovery Workbench API Specification")],
     [("05 Technical architecture", "Recovery Workbench API Specification", "dir")], "split by x-module + ownership.json api; each operation in exactly one file; gateway-bff and index; asyncapi/"),
    ("B-ARCH-EVT", "Event and Messaging v-next and Kafka Topic and Event Catalog v1", [("05 Technical architecture", "Recovery Workbench Event and Messaging Design")],
     [("05 Technical architecture", "Recovery Workbench Event and Messaging Design", None), ("05 Technical architecture", "Recovery Workbench Kafka Topic and Event Catalog", ".xlsx")], "19 topics + rwb.decision-record.v1, .dlt, outbox/inbox, CloudEvents"),
    ("B-ARCH-WF", "Batch and Scheduling v-next and Temporal Workflow and Activity Catalog v1", [("05 Technical architecture", "Recovery Workbench Batch and Scheduling Design")],
     [("05 Technical architecture", "Recovery Workbench Batch and Scheduling Design", None), ("05 Technical architecture", "Recovery Workbench Temporal Workflow and Activity Catalog", ".xlsx")], "Quartz retired; each JOB to a Schedule or event-started workflow (ownership.json jobs)"),
    ("B-ARCH-DB", "Physical Schema folder v-next, LDM v-next, ERD v-next", [("06 Data", "Recovery Workbench Physical Schema"), ("06 Data", "Recovery Workbench Logical Data Model and Data Dictionary"), ("06 Data", "Recovery Workbench Entity Relationship Diagram")],
     [("06 Data", "Recovery Workbench Physical Schema", "dir"), ("06 Data", "Recovery Workbench Logical Data Model and Data Dictionary", None), ("06 Data", "Recovery Workbench Entity Relationship Diagram", None)], "19 rwb_<name>.sql + recovery_views.sql + README; FK cuts from the Ownership Map sheet"),
    ("B-ARCH-CON", "Service Contract Catalog v1", [], [("05 Technical architecture", "Recovery Workbench Service Contract Catalog", ".md"), ("05 Technical architecture", "Recovery Workbench Service Contract Catalog", ".xlsx")], "from ownership.json; include the v5 slide 13 call-type matrix"),
]

def out_path(folder, stem, ext):
    d = ROOT / folder; n = next_version(d, stem)
    if ext == "dir":
        return f"{folder}/{stem} v{n}"
    if ext is None:
        lp = latest_path(d, stem)
        ext = lp.suffix if lp and lp.is_file() else ".md"
    return f"{folder}/{stem} v{n}{ext}"

def src_path(folder, stem):
    lp = latest_path(ROOT / folder, stem)
    return str(lp.relative_to(ROOT)) if lp else None

DOC_RULES = """Do: produce the next version of each output. Keep every section, ID, number and date of the source; release dates get "(tentative)".
Change only what the realignment needs: {note}. Use the Ownership Map for every owner. New decisions use the IDs in _work/msr/plan/ids.json.
First two lines are the header in Template and Rules §R8.1. Add a change-log row "<version>, 22 November 2026, D-RCV-53 microservice realignment, T3 Code / OpenCode / DeepSeek v4.1 Flash".
How to write each format (never edit the source):
- .md: write the new file directly.
- .docx: write the full text to _work/msr/docs/{wp}/<name>.md, then: python -I "{office}" md-docx "<that md>" "<output .docx>" --template "<source .docx>"
- .xlsx: python -I "{office}" copy "<source>" "<output>" ; then add sheets/rows with: python -I "{office}" xlsx-append "<output>" "<sheet>" "<rows.json>"
- .pptx: python -I "{office}" copy "<source>" "<output>" ; then python -I "{office}" pptx-append "<output>" "<slides.md>"
- folder family: python -I "{office}" copy "<source folder>" "<output folder>" ; then for each file that changes, write its next version inside the new folder.
Never invent values: placeholders and jsonl rows as Template and Rules §R9.
"""

def doc_wp(wp, title, srcs, outs, note, agent="aisdlc-msr-worker"):
    reads = [f"- {s}" for s in srcs if s] + [f"- converted text under _work/msr/extract/ (or convert with: python -I \"{CONVERT}\" <file> _work/msr/extract/{wp})",
             f"- {TPL} (§R1, §R3, §R5, §R8, §R9)", f"- {OWN} and 22 Microservice Realignment/Recovery Workbench Microservice Ownership Map v1.xlsx",
             f"- {V5}", f"- {TD}", "- _work/msr/plan/split_plan.json (\"stats\" and \"legacy\" only)", "- _work/msr/plan/ids.json"]
    text = (f"# WP {wp} — {title}\n" + HEADER.format(agent=agent, fanout=0) + "Read only:\n" + "\n".join(reads)
            + "\nWrite only:\n" + "\n".join(f"- {o}" for o in outs)
            + f"\n- _work/msr/docs/{wp}/ (scratch)\n- _work/msr/gaps/{wp}.jsonl\n- _work/msr/assumptions/{wp}.jsonl\n- _work/msr/editlog/{wp}.md\n"
            + DOC_RULES.format(note=note, wp=wp, office=OFFICE) + FINISH.format(wp=wp))
    return {"wp": wp, "text": text, "expect": list(outs) + [f"_work/msr/editlog/{wp}.md"], "fanout": False, "agent": agent}

def req_wps():
    f3 = "03 Requirements and specifications"; out = []
    rt = read_json(WORK / "plan" / "runtime.json", {}) or {}
    brd_agent = "aisdlc-msr-worker" if rt.get("brd_fallback") else "aisdlc-brd-builder"
    prd_agent = "aisdlc-msr-worker" if rt.get("brd_fallback") else "aisdlc-prd-builder"
    for key, stem in [("PROG", "Recovery Workbench Business Requirements Program"), ("E1", "Recovery Workbench Business Requirements Epic 1"),
                      ("E2", "Recovery Workbench Business Requirements Epic 2")]:
        md = out_path(f3, stem, ".md"); docxp = md[:-3] + ".docx"
        out.append(doc_wp(f"B-REQ-BRD-{key}", f"{stem} next version (BRD Builder)", [src_path(f3, stem), "22 Microservice Realignment/aisdlc/docs/brds/"],
                          [md, docxp], "BR IDs stable, business content unchanged; add a section 'Delivery model' (19 service epics, waves, contract-first) and a BR -> service epic -> business epic trace table", brd_agent))
    stem = "Recovery Workbench Business Requirements Epics 3 to 8"
    out.append(doc_wp("B-REQ-BRD-E38", "New BRD Epics 3 to 8 v1 (BRD Builder)", [src_path(f3, "Recovery Workbench Epics 3 to 8 Specification"),
                      "17 AI-First SDLC Repository v2/docs/prds/epics-3-to-8-specification.md", "04 User stories/Recovery Workbench User Stories Epics 3 to 8 v3.md"],
                      [f"{f3}/{stem} v1.md", f"{f3}/{stem} v1.docx"], "fill business gaps of the thin stories; every missing value becomes a Q- item (-> gap row) and an ASM- item (-> assumption row)", brd_agent))
    for s in SERVICES + [{"code": "PLT", "service": "Platform", "name": "Platform"}]:
        name = f"Recovery Workbench PRD {s['code']} {s['service']} v1.md" if s["code"] != "PLT" else "Recovery Workbench PRD PLT Platform v1.md"
        out.append(doc_wp(f"B-REQ-PRD-{s['code']}", f"PRD {s['code']} {s['service']} v1 (PRD Builder)",
                          ["03 Requirements and specifications BRDs (latest versions) and their converted text in _work/msr/extract/",
                           f"FSD v6 file for module {s['code']} in _work/msr/extract/", f"Arch v5 slides for {s['service']}"],
                          [f"{f3}/PRD/{name}"], f"PRD for {s['service']}: CAP-/FR-/NFR-/AC- IDs, FR-{s['code']}-nnn mapped to the FSD REQ IDs, release slicing by wave, no design beyond confirmed v5 constraints, status Draft, empty approval table", prd_agent))
    return out

def main():
    plan = read_json(WORK / "plan" / "split_plan.json"); cap = read_json(WORK / "plan" / "capacity.json", {}) or {}
    fan = cap.get("fanout", 5)
    q = {"A10": [], "B": [], "C": [], "D": []}
    for w in story_wps(plan, fan):
        q["B"].append(w)
    q["B"] += req_wps()
    for wp, title, srcs, outs, note in ARCH:
        q["B"].append(doc_wp(wp, title, [src_path(f, s) for f, s in srcs], [out_path(f, s, e) for f, s, e in outs], note))
    docs = []
    for i, (track, folder, stem, note) in enumerate(DOCS, 1):
        src = src_path(folder, stem); out = out_path(folder, stem, None if src else ".docx")
        if src and (ROOT / src).is_dir():
            out = out_path(folder, stem, "dir")
        docs.append({"track": track, "source": src, "output": out, "note": note})
        q["B"].append(doc_wp(f"B-{track}-{i:02d}", f"{stem} next version", [src], [out], note))
    write_json(WORK / "plan" / "docs.json", docs)
    q["A10"].append(doc_wp("A10-CTX", "Update AI-SDLC workspace contexts to Arch v5 (context-updater)",
                           ["22 Microservice Realignment/aisdlc/.github/contexts/"], ["22 Microservice Realignment/aisdlc/.github/contexts/realignment-v5-context.md"],
                           "write the new context file realignment-v5-context.md and add it to context-manifest.json copy in the workspace only (the workspace is a copy, so editing its files is allowed)", "aisdlc-context-updater"))
    f4, f9, f11 = "04 User stories", "09 Testing and quality", "11 Delivery and operations"
    cat = f"{f4}/Recovery Workbench Service Story Catalog v1.xlsx"
    c_items = [
        ("C2-RTM", "RTM next version (Traceability Manager)", [src_path(f9, "Recovery Workbench Requirements Traceability Matrix"), cat], [out_path(f9, "Recovery Workbench Requirements Traceability Matrix", ".xlsx")], "all 235 requirements -> legacy key -> new story IDs -> PRD FR IDs (fragments)", "aisdlc-traceability-manager"),
        ("C3-TC", "Test Cases next version and Regression Suite next version (QA Test Case Generator)", [src_path(f9, "Recovery Workbench Test Cases"), src_path(f9, "Recovery Workbench Regression Suite"), cat], [out_path(f9, "Recovery Workbench Test Cases", ".xlsx"), out_path(f9, "Recovery Workbench Regression Suite", ".xlsx")], "add Story, Service, Level columns; -ITG copies; draft TCs only for slices with no legacy TC, tagged (new, D-RCV-53)", "aisdlc-qa-test-case-generator"),
        ("C4-BSEQ", "Build Sequence next version", [src_path(f11, "Recovery Workbench Build Sequence Epic 1 and Epic 2"), cat], [out_path(f11, "Recovery Workbench Build Sequence Epic 1 and Epic 2", None)], "by service and lane; Day 1 first", "aisdlc-msr-worker"),
        ("C4-SBO", "Story Build Order next version", [src_path(f11, "Recovery Workbench Story Build Order"), cat], [out_path(f11, "Recovery Workbench Story Build Order", None)], "lanes and Ready to start", "aisdlc-msr-worker"),
        ("C4-DEP", "Dependency Map next version", [src_path(f11, "Recovery Workbench Dependency Map"), cat], [out_path(f11, "Recovery Workbench Dependency Map", None)], "H/C/I/X classes", "aisdlc-msr-worker"),
        ("C-EPICS", "Service Epics v1", [cat], [f"{f4}/Recovery Workbench Service Epics v1.md"], "31 epics: scope, wave, suggested owner, lanes, Day-1 stories", "aisdlc-technical-documenter"),
        ("C-DEF", "Story Defects next version", [src_path(f4, "Recovery Workbench Story Defects Epic 1 Epic 2 and Enablers"), cat], [out_path(f4, "Recovery Workbench Story Defects Epic 1 Epic 2 and Enablers", ".xlsx")], "map each open defect to the new story IDs", "aisdlc-msr-worker"),
        ("C-WEX", "Worked Example next version (E1-018)", [src_path(f4, "Recovery Workbench User Story Worked Example"), cat], [out_path(f4, "Recovery Workbench User Story Worked Example", ".md")], "use Template and Rules §R7.3", "aisdlc-msr-worker"),
        ("C-ACG", "Acceptance Criteria Glossary next version", [src_path(f4, "Recovery Workbench Acceptance Criteria Glossary")], [out_path(f4, "Recovery Workbench Acceptance Criteria Glossary", ".xlsx")], "add origin tag, contract mock Given, -ITG", "aisdlc-msr-worker"),
        ("C-HTR", "How To Read The Acceptance Criteria next version", [src_path(f4, "Recovery Workbench How To Read The Acceptance Criteria")], [out_path(f4, "Recovery Workbench How To Read The Acceptance Criteria", ".docx")], "explain slices and origin tags", "aisdlc-msr-worker"),
        ("C-BN1", "Build Notes Epic 1 next version", [src_path(f4, "Recovery Workbench Build Notes Epic 1"), cat], [out_path(f4, "Recovery Workbench Build Notes Epic 1", ".md")], "per service and lane", "aisdlc-msr-worker"),
        ("C-BN2", "Build Notes Epic 2 next version", [src_path(f4, "Recovery Workbench Build Notes Epic 2"), cat], [out_path(f4, "Recovery Workbench Build Notes Epic 2", ".md")], "per service and lane", "aisdlc-msr-worker"),
        ("C-BNT", "Build Notes Technical Enablers next version", [src_path(f4, "Recovery Workbench Build Notes Technical Enablers"), cat], [out_path(f4, "Recovery Workbench Build Notes Technical Enablers", ".md")], "PLT epics", "aisdlc-msr-worker"),
    ]
    for wp, title, srcs, outs, note, agent in c_items:
        q["C"].append(doc_wp(wp, title, srcs, outs, note, agent))
    f12 = "12 Project communication"
    for wp, stem, note in [("D2-IDX", "Recovery Workbench Document Index", "new sections 'Microservice realignment' and 'Document gaps'; list every new file from all edit logs"),
                           ("D2-CTL", "Recovery Workbench Document Control Sheet", "one row per new file, label 'Document set v15'"),
                           ("D2-HUB", "Recovery Workbench Project Hub", "links to the new files; label 'Document set v15'"),
                           ("D2-TSP", "Recovery Workbench Team Start Pack", "Day-1 Work Allocation per team type; no names"),
                           ("D2-CTO", "Recovery Workbench Executive Presentation CTO", "diagram-led slides: services, waves, Day-1, gaps"),
                           ("D2-OVR", "Recovery Workbench Project Overview", "realignment summary")]:
        q["D"].append(doc_wp(wp, f"{stem} next version", [src_path(f12, stem), "_work/msr/editlog/"], [out_path(f12, stem, None)], note))
    for name, items in q.items():
        out = []
        for w in items:
            p = WORK / "wp" / f"{w['wp']}.md"; p.write_text(w["text"], encoding="utf-8")
            out.append({"wp": w["wp"], "agent": w["agent"], "file": str(p.relative_to(ROOT)), "fanout": w["fanout"], "expect": w["expect"]})
        write_json(WORK / "wp" / f"queue-{name}.json", out)
    print("A7b OK", {k: len(v) for k, v in q.items()})

if __name__ == "__main__":
    main()
```

- [ ] **Step 5: Run the tests, then the generator.**

```powershell
python -I "22 Microservice Realignment/compat/make_wps.py"
```

Expected: tests OK, then `A7b OK {'A10': 1, 'B': <about 140–230>, 'C': 13, 'D': 6}`.

Check the queue-B count: it is the story WPs plus 24 REQ, 8 ARCH and 49 document families. Open one story WP file and one document WP file and confirm two things:
- Every path under "Write only" is a new file.
- No path under "Write only" points into folders 17, 18 or 21.

---

### Task 14: Run documents — Template and Rules, Change Register, Tracker, Jira impact file, Run Summary (step A8)

**Files:**
- Create: `22 Microservice Realignment/compat/docgen.py`
- Test: `22 Microservice Realignment/compat/tests/test_docgen.py`
- Output (all in `22 Microservice Realignment/`):
  - `Recovery Workbench Microservice Story Template and Rules v1.md`. Its text is cut from the ROOT plan copy, Appendix R, between the R-TEMPLATE markers.
  - `Recovery Workbench Microservice Change Register v1.md`
  - `Recovery Workbench Microservice Realignment Tracker v<n>.xlsx`, with a new version on every call
  - `Recovery Workbench Jira Impact and Follow-up v1.md`. Its text is cut from Appendix R between the R-JIRA markers, plus computed scale tables. **This is the only output file allowed to say "Jira".**
  - `Recovery Workbench Realignment Run Summary v1.md`, written in Task 21

- [ ] **Step 1: Write the failing test.**

```python
import unittest
import docgen as dg

TXT = "a\n<!-- R-TEMPLATE-BEGIN -->\n## R1\nx\n<!-- R-TEMPLATE-END -->\nb\n<!-- R-TEMPLATE-BEGIN -->\n## R3\ny\n<!-- R-TEMPLATE-END -->\n"

class TestDocgen(unittest.TestCase):
    def test_blocks(self):
        out = dg.blocks(TXT, "R-TEMPLATE")
        self.assertIn("## R1", out); self.assertIn("## R3", out); self.assertNotIn("b\n", out)
        with self.assertRaises(SystemExit):
            dg.blocks(TXT, "R-JIRA")

    def test_jira_rows(self):
        legacy = {"RWB-E1-014": {"disposition": "Retired (D-RCV-53)", "slices": []},
                  "RWB-E1-042": {"disposition": "Preserved + delta", "slices": ["RWB-P3-E1042-APP", "RWB-P3-E1042-CON", "RWB-PLT-E1042-CON"]},
                  "N001": {"disposition": "New", "slices": ["RWB-PLT-N001-CON"]}}
        rows = dg.jira_rows(legacy)
        act = {r[0]: r[2] for r in rows}
        self.assertTrue(act["RWB-E1-014"].startswith("Close"))
        self.assertTrue(act["RWB-E1-042"].startswith("Keep"))
        self.assertTrue(act["N001"].startswith("Create"))
        self.assertEqual([r for r in rows if r[0] == "RWB-E1-042"][0][3], 2)
```

- [ ] **Step 2: Run the tests.** Expected: FAIL (import error).

- [ ] **Step 3: Write `docgen.py`.**

```python
"""Run documents for D-RCV-53. Never overwrites: v1 files are kept if present; the Tracker gets a new version each call."""
import argparse, collections, re, sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
from common import ROOT, R22, R23, WORK, SERVICES, OWNER, header, next_version, read_json, read_jsonl
from xlsx_write import write_book

PLAN = ROOT / "2026-11-22-recovery-microservice-realignment-implementation-plan.md"
TOOL = "Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash. Decision D-RCV-53."
REASON = {
    "RWB-E1-014": "Decision log copy to the data lake. Arch v5 has no data lake (ADR-018); reporting reads events into the rwb-reporting read model.",
    "RWB-TE-007": "Quartz scheduler. Retired by Arch v5; Temporal Schedules through the workflow kit replace it (RWB-PLT-E1071-CON, ADR-016).",
    "RWB-E1-001": ("In build: creates the single recovery schema (92 tables, 14 data products, dictionary). Arch v5 needs one rwb_<name> schema per "
                   "service. The built migration is kept unchanged; the split is new work in RWB-PLT-NF06-DB and the per-service DB stories, "
                   "and each table moves to its owner schema by the Ownership Map. Only change if absolutely needed (U2)."),
}
DISP_TEXT = {
    "Retired (D-RCV-53)": "Retired by the realignment.",
    "Already retired": "Already cancelled before the realignment; no new story.",
    "Preserved + delta": "Built or in build. As-built story kept word for word; the microservice change is a separate delta story.",
    "Must change": "In build and must change to fit Arch v5.",
    "Moved (no impact)": "Moved to its service epic; content unchanged.",
    "Split (rework)": "Split into linked stories by service and team type.",
    "New": "New story created by the realignment.",
}

def blocks(text, name):
    found = re.findall(r"<!-- " + re.escape(name) + r"-BEGIN -->\n(.*?)<!-- " + re.escape(name) + r"-END -->", text, re.S)
    if not found:
        raise SystemExit(f"markers {name} not found")
    return "\n".join(b.strip() + "\n" for b in found)

def _write_once(path, text):
    if path.exists():
        print("KEPT", path.name); return path
    path.write_text(text, encoding="utf-8"); print("WROTE", path.name); return path

def template():
    body = blocks(PLAN.read_text(encoding="utf-8"), "R-TEMPLATE")
    return _write_once(R22 / "Recovery Workbench Microservice Story Template and Rules v1.md",
                       f"# Recovery Workbench Microservice Story Template and Rules v1\n\n{header()}\n{TOOL}\n\n{body}")

def _plan():
    return read_json(WORK / "plan" / "split_plan.json"), {r["key"]: r for r in read_json(WORK / "plan" / "legacy_index.json")}

def change_register():
    plan, idx = _plan(); s = {x["id"]: x for x in plan["slices"]}
    lines = [f"# Recovery Workbench Microservice Change Register v1\n\n{header()}\n{TOOL}\n",
             "One row per legacy story. Built and in-build Epic 1 work is not changed unless absolutely needed (U2).\n",
             "## Summary\n", "| Disposition | Legacy stories | Meaning |", "|---|---|---|"]
    cnt = collections.Counter(v["disposition"] for v in plan["legacy"].values())
    lines += [f"| {d} | {n} | {DISP_TEXT.get(d, '')} |" for d, n in sorted(cnt.items())]
    lines += ["\n## Stories\n", "| Legacy key | Title | Disposition | Build status | New stories | Reason |", "|---|---|---|---|---|---|"]
    for k, v in sorted(plan["legacy"].items()):
        title = idx.get(k, {}).get("title") or (s[v["slices"][0]]["title"] if v["slices"] else "")
        bs = s[v["slices"][0]]["build_status"] if v["slices"] else ("Built" if k in REASON else "Not started")
        lines.append(f"| {k} | {title.replace('|', '/')} | {v['disposition']} | {bs} | {', '.join(v['slices']) or 'None'} | "
                     f"{REASON.get(k, DISP_TEXT.get(v['disposition'], ''))} |")
    return _write_once(R22 / "Recovery Workbench Microservice Change Register v1.md", "\n".join(lines) + "\n")

def jira_rows(legacy):
    rows = []
    for k, v in sorted(legacy.items()):
        d, n = v["disposition"], len(v["slices"])
        if d.startswith("Retired"):
            act, new = "Close the issue as won't do (retired by D-RCV-53); no new issues", 0
        elif d == "Already retired":
            act, new = "No change (already cancelled)", 0
        elif d in ("Preserved + delta", "Must change"):
            act, new = "Keep the issue and its status; link the new delta and contract issues", max(0, n - 1)
        elif d == "Moved (no impact)":
            act, new = "Keep the issue; change its epic link to the service epic", max(0, n - 1)
        elif d == "New":
            act, new = "Create the issue in its service, platform or integration epic", n
        else:
            act, new = "Keep the issue as the main APP story; create the linked split issues; move it to the service epic", max(0, n - 1)
        rows.append([k, d, act, new, ", ".join(v["slices"])])
    return rows

def jira():
    plan, _ = _plan(); rows = jira_rows(plan["legacy"])
    body = blocks(PLAN.read_text(encoding="utf-8"), "R-JIRA")
    epics = collections.Counter(x["epic"] for x in plan["slices"])
    scale = collections.Counter(r[1] for r in rows); new_total = sum(r[3] for r in rows)
    t = [f"# Recovery Workbench Jira Impact and Follow-up v1\n\n{header()}\n{TOOL}\n", body,
         "\n## Scale\n", f"- Epics to create: {len(epics)} (7 platform, 19 service, 5 integration).",
         f"- Issues to create: {new_total}. Issues to close: {scale.get('Retired (D-RCV-53)', 0)}.", "",
         "| Disposition | Legacy issues |", "|---|---|"] + [f"| {d} | {n} |" for d, n in sorted(scale.items())]
    t += ["\n## Epics\n", "| Epic | Stories |", "|---|---|"] + [f"| {e} | {n} |" for e, n in sorted(epics.items())]
    t += ["\n## Per legacy issue\n", "| Legacy key | Disposition | Follow-up action | New issues | New story IDs |", "|---|---|---|---|---|"]
    t += [f"| {r[0]} | {r[1]} | {r[2]} | {r[3]} | {r[4]} |" for r in rows]
    return _write_once(R22 / "Recovery Workbench Jira Impact and Follow-up v1.md", "\n".join(t) + "\n")

def tracker():
    plan, idx = _plan(); docs = read_json(WORK / "plan" / "docs.json", []) or []
    ids = read_json(WORK / "plan" / "ids.json", {}) or {}; own = read_json(WORK / "plan" / "ownership.json", {}) or {}
    st = read_json(WORK / "status.json", {}) or {}
    logs = sorted((WORK / "editlog").glob("*.md"))
    defects = read_jsonl(WORK / "plan" / "defects.jsonl")
    sheets = {
        "Documents": (["Track", "Source", "Output", "Change"], [[d["track"], d["source"], d["output"], d["note"]] for d in docs]),
        "Stories": (["Story", "Title", "Work type", "Epic", "Lane", "Ready", "Suggested owner", "Wave", "Business epic", "Legacy", "File"],
                    [[x["id"], x["title"], x["wt"], x["epic"], x.get("lane"), x["ready"], OWNER[x["owner"]], x["wave"], x["business_epic"], x["legacy"], x["file"]] for x in plan["slices"]]),
        "Story split": (["Legacy key", "Title", "Disposition", "New stories"], [[k, idx.get(k, {}).get("title", ""), v["disposition"], v["slices"]] for k, v in sorted(plan["legacy"].items())]),
        "Decisions": (["Item", "Value"], [["Realignment decision", ids.get("realignment_decision")], ["ADRs", ids.get("adrs")], ["Decision log rows", ids.get("dl")]]),
        "Rulings": (["Item", "Owner", "Ruling", "Assumption"], own.get("rulings", [])),
        "Defects": (["Defect", "Legacy story", "New story", "Note"], [[d.get("id"), d.get("legacy"), d.get("story"), d.get("note")] for d in defects]),
        "Edit log": (["WP", "File"], [[p.stem, str(p.relative_to(ROOT))] for p in logs]),
        "WP status": (["WP", "State", "Tries"], [[k, v.get("state"), v.get("tries")] for k, v in sorted(st.items())]),
    }
    n = next_version(R22, "Recovery Workbench Microservice Realignment Tracker")
    out = R22 / f"Recovery Workbench Microservice Realignment Tracker v{n}.xlsx"
    write_book(out, sheets, read_me=header() + f"\nRecovery Workbench Microservice Realignment Tracker v{n}\n{TOOL}\nStatus at generation time; regenerate for a new version.")
    print("WROTE", out.name); return out

def summary():
    plan, _ = _plan(); st = read_json(WORK / "status.json", {}) or {}; cap = read_json(WORK / "plan" / "capacity.json", {}) or {}
    states = collections.Counter(v.get("state") for v in st.values())
    rep = sorted((R22 / "checks" / "reports").glob("full-*.md"))
    gaps = sorted(R23.glob("Recovery Workbench Gap Register v*.md")); asms = sorted(R23.glob("Recovery Workbench Assumptions Register v*.md"))
    t = [f"# Recovery Workbench Realignment Run Summary v1\n\n{header()}\n{TOOL}\n",
         "## Capacity used\n", f"- Budget (live model sessions): {cap.get('budget')}; fanout per story WP: {cap.get('fanout')}; probe process max: {cap.get('process_max')}; subagents per session: {cap.get('session_subagent_max')}.",
         "\n## Work packages\n"] + [f"- {k}: {v}" for k, v in sorted(states.items(), key=lambda kv: str(kv[0]))]
    t += ["\n## Stories\n", f"- Stories: {plan['stats']['slices']}; legacy keys: {plan['stats']['legacy']}; Day-1 stories: {plan['stats']['day1']}; lanes: {plan['stats']['lanes']}.",
          f"- Team types with Day-1 work: {', '.join(plan['stats']['day1_teams'])}.",
          "\n## Registers\n", f"- Gap Register: {gaps[-1].name if gaps else 'not written'}", f"- Assumptions Register: {asms[-1].name if asms else 'not written'}",
          "\n## Checks\n", f"- Last full report: {rep[-1].name if rep else 'not run'}",
          "\n## Next\n", "- The verification loop is a separate, later activity (U8). This run made no human stops."]
    return _write_once(R22 / "Recovery Workbench Realignment Run Summary v1.md", "\n".join(t) + "\n")

if __name__ == "__main__":
    ap = argparse.ArgumentParser(); ap.add_argument("cmd", choices=["template", "change", "jira", "tracker", "summary", "a8"]); a = ap.parse_args()
    if a.cmd == "a8":
        template(); change_register(); jira(); tracker()
    else:
        {"template": template, "change": change_register, "jira": jira, "tracker": tracker, "summary": summary}[a.cmd]()
```

- [ ] **Step 4: Run the tests, then step A8.**

```powershell
python -I "22 Microservice Realignment/compat/docgen.py" a8
```

Expected: tests OK, then four `WROTE` lines: Template and Rules v1, Change Register v1, Jira Impact and Follow-up v1 and Tracker v1.

Open the Template and Rules v1 file and confirm two things:
- It contains `### R7.2` with the 19 section names.
- It does not contain the word "Jira".

---

### Task 15: Gap and Assumptions registers — seed rows and D1 numbering

**Files:**
- Create: `22 Microservice Realignment/compat/number_registers.py`
- Test: `22 Microservice Realignment/compat/tests/test_number_registers.py`
- Output:
  - `_work/msr/gaps/SEED.jsonl` and `_work/msr/assumptions/SEED.jsonl` (step A9, now)
  - In step D1 (Task 21):
    - `23 Document Gaps/Recovery Workbench Gap Register v<n>.xlsx` and `.md`
    - `23 Document Gaps/Recovery Workbench Assumptions Register v<n>.xlsx` and `.md`
    - `_work/msr/plan/register_map.json`

**How a WP writes a candidate row.** Agents add one JSON object per line. Scripts call `common.add_gap` and `common.add_asm`. Example lines:

```json
{"id": "CG-B-P3-01-1", "title": "RPO not stated for rwb-case", "source": "03 Requirements and specifications/Recovery Workbench Non Functional Specification v5.docx", "section": "4.2", "description": "No RPO value for the case service", "evidence": "Section 4.2 lists RTO only", "type": "Missing", "area": "NFR", "severity": "P2", "needed_by_wave": "1", "legacy_ref": "RWB-E1-018", "owner_role": "Solution architect", "asm": "ASM-B-P3-01-1", "proposed": "Confirm RPO per service", "wp": "B-P3-01"}
{"id": "ASM-B-P3-01-1", "text": "rwb-case RPO is the programme RPO", "why": "no per-service value", "read": "NFR Specification 4.2", "gap": "CG-B-P3-01-1", "applied_in": "RWB-P3-E1018-APP", "confidence": "Medium", "confirm": "Solution architect confirms", "impact": "Backup schedule changes", "wp": "B-P3-01"}
```

- [ ] **Step 1: Write the failing test.**

```python
import json, tempfile, unittest
from pathlib import Path
import number_registers as nr

class TestNumber(unittest.TestCase):
    def test_number_dedupe_rewrite(self):
        gaps = [{"id": "CG-A-1", "title": "RPO missing", "legacy_ref": "", "severity": "P2", "wp": "A"},
                {"id": "CG-B-2", "title": "RPO  missing", "legacy_ref": "", "severity": "P1", "wp": "B"},
                {"id": "CG-B-3", "title": "Env names", "legacy_ref": "", "severity": "P3", "wp": "B"}]
        asms = [{"id": "ASM-A-1", "text": "Use programme RPO", "gap": "CG-A-1", "wp": "A"},
                {"id": "ASM-B-1", "text": "use programme rpo", "gap": "CG-B-2", "wp": "B"}]
        g, a, m = nr.number(gaps, asms)
        self.assertEqual([x["id"] for x in g], ["GAP-0001", "GAP-0002"])
        self.assertEqual(g[0]["severity"], "P1"); self.assertEqual(g[0]["raised_by"], "A; B")
        self.assertEqual(m["CG-B-2"], "GAP-0001"); self.assertEqual(m["ASM-B-1"], "ASM-0001")
        self.assertEqual(a[0]["gap"], "GAP-0001")
        self.assertEqual(nr.rewrite_text("see CG-B-3 and ASM-A-1; CG-X-9", m), "see GAP-0002 and ASM-0001; CG-X-9")
        with tempfile.TemporaryDirectory() as d:
            p = Path(d) / "s.md"; p.write_text("Not specified (CG-A-1; ASM-A-1)", encoding="utf-8")
            self.assertEqual(nr.rewrite_file(p, m), 1)
            self.assertEqual(p.read_text(encoding="utf-8"), "Not specified (GAP-0001; ASM-0001)")
```

- [ ] **Step 2: Run the tests.** Expected: FAIL (import error).

- [ ] **Step 3: Write `number_registers.py`.**

```python
"""--seed: known gaps/assumptions (A9). default (D1): merge all candidates, dedupe, number, rewrite citations, write registers."""
import argparse, json, re, sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
from common import ROOT, R23, F18, WORK, header, next_version, read_json, read_jsonl, write_json, reset_cands, add_gap, add_asm
from xlsx_write import write_book

SEV = {"P1": 1, "P2": 2, "P3": 3}
CITE = re.compile(r"\b(?:CG|ASM)-[A-Za-z0-9]+(?:-[A-Za-z0-9]+)*-\d+\b|\bASM-seed\b|\bASM-A6-fallback\b")
G_HEAD = ["GAP ID", "Title", "Source", "Section", "Description", "Evidence", "Type", "Area", "Severity", "Needed by wave",
          "Legacy ref", "Owner role", "Assumption", "Proposed resolution", "Raised by", "Status"]
A_HEAD = ["ASM ID", "Assumption", "Why", "What was read", "Gap", "Applied in", "Confidence", "How to confirm", "Impact if wrong", "Raised by", "Status"]

SEED_GAPS = [  # title, description, type, severity, area, owner role, needed by wave
    ("RPO and RTO per service not stated", "The NFR Specification and Availability design give programme targets only; Arch v5 has 19 services.", "Missing", "P1", "NFR", "Solution architect", "1"),
    ("Environment names for per-service deployment", "Environment and Deployment Design names environments for one service only.", "Missing", "P2", "Infrastructure", "SCB IT infrastructure lead", "0"),
    ("'Weeks' versus '28 days' retention wording", "The NFR Specification uses both wordings for the same period.", "Conflict", "P2", "NFR", "Business analyst", "1"),
    ("Kafka cluster ownership and sizing", "Arch v5 names Kafka but not which team provisions and sizes the cluster.", "Missing", "P1", "Infrastructure", "SCB IT infrastructure lead", "0"),
    ("Temporal namespace and codec key ownership", "The Temporal and Drools design does not name who issues the codec key.", "Missing", "P2", "Infrastructure", "SCB IT infrastructure lead", "0"),
    ("Schema registry product", "BACKWARD compatibility is required; the registry product is not named.", "Missing", "P2", "Platform", "Solution architect", "0"),
    ("Non-feature tasks NF-01..NF-08 have no story master", "The NF tasks exist only as titles; content is drafted from Arch v5.", "Missing", "P2", "Stories", "Delivery lead", "0"),
    ("Partner gateway hosting (DMZ)", "Arch v5 places the partner gateway in the DMZ; the hosting team and product are not named.", "Missing", "P2", "Infrastructure", "SCB IT infrastructure lead", "4"),
    ("Issue tracker status of Epic 1 not readable in this run", "Build status is taken from the realignment plan, not from the tracker (U6).", "Missing", "P3", "Delivery", "Delivery lead", "1"),
]
SEED_ASMS = [  # text, why, confidence
    ("Parameters and reference data (E1-042, E1-043) are owned by rwb-case", "R-PREC default ruling", "Medium"),
    ("The case list API is owned by rwb-case", "R-PREC default ruling", "Medium"),
    ("The rule package registry is owned by rwb-decision", "R-PREC default ruling", "Medium"),
    ("The interaction ledger is owned by rwb-source-data", "R-PREC default ruling", "Medium"),
    ("Feature flags are a platform library", "R-PREC default ruling", "Medium"),
    ("Release dates are kept unchanged and are tentative; the programme finishes within 8 months", "user decision U7", "High"),
    ("Ownership is a suggestion only; any team may pick up any story", "user decision U3", "High"),
    ("All AI-drafted documents stay in Draft status until the later verification loop", "user decision U8", "High"),
]

def seed():
    reset_cands("SEED")
    for i, (t, d, ty, sv, ar, ow, wv) in enumerate(SEED_GAPS):
        a = add_asm("SEED", f"Until resolved, the plan default is used for: {t}", "seed gap", read="Arch v5, NFR Specification",
                    confidence="Low", confirm=f"{ow} confirms", impact="Stories and documents citing this item change")
        add_gap("SEED", t, d, gtype=ty, severity=sv, area=ar, owner_role=ow, asm=a, needed_by_wave=wv,
                source="Realignment plan Appendix R", proposed="Confirm in the verification loop")
    for t, why, c in SEED_ASMS:
        add_asm("SEED", t, why, read="Realignment plan Appendix R §R1 and §R3", confidence=c, confirm="Product owner or architect confirms")
    print("A9 SEED OK", len(SEED_GAPS), "gaps", len(SEED_GAPS) + len(SEED_ASMS), "assumptions")

def _norm(s):
    return re.sub(r"[^a-z0-9]+", " ", str(s or "").lower()).strip()

def number(gaps, asms):
    m, out_g, by = {}, [], {}
    for g in gaps:
        key = (_norm(g.get("title")), _norm(g.get("legacy_ref")))
        if key in by:
            t = by[key]
            if SEV.get(g.get("severity"), 3) < SEV.get(t.get("severity"), 3):
                t["severity"] = g["severity"]
            if g.get("wp") and g["wp"] not in t["raised_by"].split("; "):
                t["raised_by"] += "; " + g["wp"]
        else:
            t = dict(g); t["raised_by"] = g.get("wp", ""); t["id"] = f"GAP-{len(out_g) + 1:04d}"; t["status"] = "Open"
            by[key] = t; out_g.append(t)
        m[g["id"]] = t["id"]
    out_a, bya = [], {}
    for a in asms:
        key = _norm(a.get("text"))
        if key in bya:
            t = bya[key]
            if a.get("wp") and a["wp"] not in t["raised_by"].split("; "):
                t["raised_by"] += "; " + a["wp"]
        else:
            t = dict(a); t["raised_by"] = a.get("wp", ""); t["id"] = f"ASM-{len(out_a) + 1:04d}"; t["status"] = "Unconfirmed"
            bya[key] = t; out_a.append(t)
        m[a["id"]] = t["id"]
    for t in out_a:
        t["gap"] = m.get(t.get("gap"), t.get("gap", ""))
    for t in out_g:
        t["asm"] = m.get(t.get("asm"), t.get("asm", ""))
    seed_asm = next((t["id"] for t in out_a if "R-PREC default ruling" in t.get("why", "")), "")
    m.setdefault("ASM-seed", seed_asm)
    fb = next((t["id"] for t in out_a if "most frequent legacy module" in t.get("text", "")), "")
    m.setdefault("ASM-A6-fallback", fb)
    return out_g, out_a, m

def rewrite_text(text, m):
    return CITE.sub(lambda x: m.get(x.group(0)) or x.group(0), text)

def rewrite_file(p, m):
    """Rewrite citations in a file created by this run. Returns 1 if changed."""
    p = Path(p); ext = p.suffix.lower()
    if ext in (".md", ".json", ".yaml", ".yml", ".sql", ".txt", ".excalidraw", ".svg"):
        old = p.read_text(encoding="utf-8", errors="replace"); new = rewrite_text(old, m)
        if new != old:
            p.write_text(new, encoding="utf-8"); return 1
        return 0
    if ext == ".xlsx":
        import openpyxl
        wb = openpyxl.load_workbook(p); ch = 0
        for ws in wb.worksheets:
            for row in ws.iter_rows():
                for c in row:
                    if isinstance(c.value, str) and CITE.search(c.value):
                        c.value = rewrite_text(c.value, m); ch = 1
        if ch:
            wb.save(p)
        return ch
    if ext == ".docx":
        import docx
        d = docx.Document(p); ch = 0
        paras = list(d.paragraphs) + [pp for t in d.tables for r in t.rows for c in r.cells for pp in c.paragraphs]
        for para in paras:
            if CITE.search(para.text):
                new = rewrite_text(para.text, m)
                for i, r in enumerate(para.runs):
                    r.text = new if i == 0 else ""
                ch = 1
        if ch:
            d.save(p)
        return ch
    return 0

def _run_outputs():
    """Every file this run created: queue expect lists + fragments + the split plan story files. Never a baseline file."""
    base = read_json(WORK / "plan" / "baseline.json", {}) or {}
    out = set()
    for q in (WORK / "wp").glob("queue-*.json"):
        for item in json.loads(q.read_text(encoding="utf-8")):
            out.update(item.get("expect", []))
    out.update(str(p.relative_to(ROOT)).replace("\\", "/") for p in (WORK / "fragments").glob("*.json"))
    plan = read_json(WORK / "plan" / "split_plan.json", {}) or {}
    out.update(x["file"] for x in plan.get("slices", []))
    files = []
    for rel in sorted(out):
        p = ROOT / rel
        if rel in base:
            continue
        files += [f for f in p.rglob("*") if f.is_file()] if p.is_dir() else ([p] if p.exists() else [])
    return files

def _imported():
    p = F18 / "aisdlc" / "DOCUMENT-GAPS.md"
    if not p.exists():
        return ["Source"], []
    rows = [[c.strip() for c in l.strip().strip("|").split("|")] for l in p.read_text(encoding="utf-8").splitlines() if l.startswith("|")]
    rows = [r for r in rows if not all(set(c) <= set("-: ") for c in r)]
    if not rows:
        return ["Source"], []
    w = max(len(r) for r in rows)
    return rows[0] + [""] * (w - len(rows[0])), [r + [""] * (w - len(r)) for r in rows[1:]]

def _md(title, head, rows):
    t = [f"# {title}\n", header(), "Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash. Decision D-RCV-53.\n",
         "| " + " | ".join(head) + " |", "|" + "---|" * len(head)]
    t += ["| " + " | ".join(str(v if v is not None else "").replace("|", "/").replace("\n", " ") for v in r) + " |" for r in rows]
    return "\n".join(t) + "\n"

def d1():
    gaps = [g for p in sorted((WORK / "gaps").glob("*.jsonl")) for g in read_jsonl(p)]
    asms = [a for p in sorted((WORK / "assumptions").glob("*.jsonl")) for a in read_jsonl(p)]
    g, a, m = number(gaps, asms)
    write_json(WORK / "plan" / "register_map.json", m)
    gr = [[x["id"], x.get("title"), x.get("source"), x.get("section"), x.get("description"), x.get("evidence"), x.get("type"), x.get("area"),
           x.get("severity"), x.get("needed_by_wave"), x.get("legacy_ref"), x.get("owner_role"), x.get("asm"), x.get("proposed"), x["raised_by"], x["status"]] for x in g]
    ar = [[x["id"], x.get("text"), x.get("why"), x.get("read"), x.get("gap"), x.get("applied_in"), x.get("confidence"), x.get("confirm"),
           x.get("impact"), x["raised_by"], x["status"]] for x in a]
    ih, irows = _imported()
    ng = next_version(R23, "Recovery Workbench Gap Register"); na = next_version(R23, "Recovery Workbench Assumptions Register")
    gt, at = f"Recovery Workbench Gap Register v{ng}", f"Recovery Workbench Assumptions Register v{na}"
    write_book(R23 / f"{gt}.xlsx", {"Gaps": (G_HEAD, gr), "Imported": (ih, irows)}, read_me=header() + f"\n{gt}. Imported sheet: read-only copy of 18 E2E Recovery Workbench/aisdlc/DOCUMENT-GAPS.md.")
    write_book(R23 / f"{at}.xlsx", {"Assumptions": (A_HEAD, ar)}, read_me=header() + f"\n{at}.")
    (R23 / f"{gt}.md").write_text(_md(gt, G_HEAD, gr), encoding="utf-8")
    (R23 / f"{at}.md").write_text(_md(at, A_HEAD, ar), encoding="utf-8")
    changed = sum(rewrite_file(p, m) for p in _run_outputs())
    left = 0
    for p in _run_outputs():
        if p.suffix.lower() in (".md", ".json"):
            left += len(CITE.findall(p.read_text(encoding="utf-8", errors="replace")))
    print(f"D1 OK gaps={len(g)} (from {len(gaps)}) assumptions={len(a)} (from {len(asms)}) files_rewritten={changed} unmapped_citations={left}")

if __name__ == "__main__":
    ap = argparse.ArgumentParser(); ap.add_argument("--seed", action="store_true"); a = ap.parse_args()
    seed() if a.seed else d1()
```

- [ ] **Step 4: Run the tests, then the seed (step A9).**

```powershell
python -I "22 Microservice Realignment/compat/number_registers.py" --seed
```

Expected: tests OK, then `A9 SEED OK 9 gaps 17 assumptions`. Numbering runs later, in Task 21 (D1).

---

### Task 16: Checks C01–C20

**Files:**
- Create: `22 Microservice Realignment/checks/run_all.py`
- Test: `22 Microservice Realignment/compat/tests/test_checks.py`
- Output: `22 Microservice Realignment/checks/reports/<mode>-<timestamp>.md` and `.json`

**Modes:**

| Mode | Checks | Scope |
|---|---|---|
| `--wp <WP> --quick` | C02, C03, C05, C12, C13, C18 | Files under "Write only" in that WP file |
| `--stage B\|C\|D` | Stage set (see `STAGES` in the code) | All outputs of that queue |
| `--full` | C01–C20 | Everything |

The exit code is 1 if any check FAILs. A WARN result never fails the run.

C12 reads the person-name deny-list from folder 21 **in memory only**. It never prints, logs or writes a name: it reports only the file, the line number and the count.

- [ ] **Step 1: Write the failing test.**

```python
import sys, tempfile, unittest
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "checks"))
import run_all as ra

def story(extra_meta="", sections=None):
    meta = "\n".join(f"| {r} | x |" for r in ra.META_ROWS)
    secs = sections or ra.SECTIONS
    body = "\n".join(f"### {i}. {s}\n\ntext\n" for i, s in enumerate(secs, 1))
    return f"# RWB-P3-E1018-APP Title\n\n| Item | Value |\n|---|---|\n{meta}\n{extra_meta}\n\n{body}\nScenario: AC1 x (legacy RWB-E1-018 AC1)\n"

class TestChecks(unittest.TestCase):
    def test_c02_c03_c05(self):
        with tempfile.TemporaryDirectory() as d:
            p = Path(d) / "s.md"; p.write_text(story(), encoding="utf-8")
            self.assertEqual(ra.c02([p])[0], "PASS"); self.assertEqual(ra.c03([p])[0], "PASS"); self.assertEqual(ra.c05([p])[0], "PASS")
            p.write_text(story(sections=ra.SECTIONS[:-1]).replace("(legacy RWB-E1-018 AC1)", ""), encoding="utf-8")
            self.assertEqual(ra.c03([p])[0], "FAIL"); self.assertEqual(ra.c05([p])[0], "FAIL")

    def test_c12_names_not_printed(self):
        with tempfile.TemporaryDirectory() as d:
            p = Path(d) / "s.md"; p.write_text("Owner: Somchai Example\n", encoding="utf-8")
            res = ra.c12([p], names={"somchai example"})
            self.assertEqual(res[0], "FAIL"); self.assertNotIn("Somchai", " ".join(res[1]))

    def test_c13(self):
        with tempfile.TemporaryDirectory() as d:
            p = Path(d) / "s.md"; p.write_text("Update the Jira issue\n", encoding="utf-8")
            self.assertEqual(ra.c13([p])[0], "FAIL")
```

- [ ] **Step 2: Run the tests.** Expected: FAIL (import error).

- [ ] **Step 3: Write `checks/run_all.py`.**

```python
"""Checks C01-C20 for the D-RCV-53 realignment. Read-only except the report files."""
import argparse, csv, json, re, sys, time
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "compat"))
from common import ROOT, R22, WORK, SERVICES, ID_RE, LEGACY_RE, sha256, read_json, read_jsonl

META_ROWS = ["Story key", "Work type", "Suggested owner", "Service", "Service epic", "Wave", "Business epic", "Release",
             "Legacy key", "Legacy disposition", "Build status", "Patterns applied", "Parallel lane", "Ready to start",
             "Depends on (build)", "Contract dependencies", "Integration dependencies", "External dependencies", "PRD reference", "Status"]
SECTIONS = ["Story", "Business rationale", "Preconditions", "Flow", "Exception paths", "INVEST check", "Acceptance criteria",
            "Business rules", "State transitions", "Authority", "Data", "Contract", "Solution plan", "Validation and messages",
            "Screens and states", "Test cases", "Guardrails", "Traceability", "Out of scope"]
SHORTS = {s["short"] for s in SERVICES}
TOOL = "T3 Code / OpenCode / DeepSeek v4.1 Flash"
JIRA_OK = {"Recovery Workbench Jira Impact and Follow-up v1.md"}
STAGES = {"B": ["C02", "C03", "C04", "C05", "C06", "C07", "C08", "C12", "C13", "C14", "C15", "C16", "C17", "C20"],
          "C": ["C09", "C10", "C11", "C12", "C13", "C19"], "D": ["C01", "C12", "C13", "C17", "C19", "C20"]}
QUICK = ["C02", "C03", "C05", "C12", "C13", "C18"]

def _t(p):
    return Path(p).read_text(encoding="utf-8", errors="replace")

def _plan():
    return read_json(WORK / "plan" / "split_plan.json", {"slices": [], "legacy": {}})

def _stories(files):
    return [Path(f) for f in files if Path(f).suffix == ".md" and re.match(r"^RWB ", Path(f).name)]

def _frags():
    return {p.stem: json.loads(p.read_text(encoding="utf-8")) for p in (WORK / "fragments").glob("*.json")}

def _res(fails, warn=False):
    return ("PASS", []) if not fails else (("WARN" if warn else "FAIL"), fails[:200])

def c01(files=None):
    base = read_json(WORK / "plan" / "baseline.json", {}) or {}
    bad = [k for k, h in base.items() if not (ROOT / k).exists() or sha256(ROOT / k) != h]
    return _res([f"changed or missing: {k}" for k in bad])

def c02(files):
    fails = []
    for p in _stories(files):
        t = _t(p); m = re.match(r"^# (\S+)", t)
        if not m or not ID_RE.match(m.group(1)):
            fails.append(f"{p.name}: title line must start with a valid story ID")
        rows = re.findall(r"^\|\s*([^|]+?)\s*\|", t.split("### 1.", 1)[0], re.M)
        got = [r for r in rows if r in META_ROWS]
        if got != META_ROWS:
            fails.append(f"{p.name}: metadata rows missing or out of order: {[r for r in META_ROWS if r not in got][:5]}")
    return _res(fails)

def c03(files):
    fails = []
    for p in _stories(files):
        heads = re.findall(r"^### (\d+)\. (.+?)\s*$", _t(p), re.M)
        if [h[1] for h in heads[:19]] != SECTIONS or [int(h[0]) for h in heads[:19]] != list(range(1, 20)):
            fails.append(f"{p.name}: the 19 section headings are not complete and in order")
    return _res(fails)

def c04(files=None):
    return _res([f"missing story file: {x['file']}" for x in _plan()["slices"] if not (ROOT / x["file"]).exists()])

def c05(files):
    fails = []
    for p in _stories(files):
        for line in _t(p).splitlines():
            if re.match(r"^\s*Scenario:\s*AC\d+", line) and not re.search(r"\((legacy RWB-[A-Z0-9-]+ AC\d+|new, D-RCV-53)\)", line):
                fails.append(f"{p.name}: AC line without origin tag: {line.strip()[:80]}")
    return _res(fails)

def c06(files=None):
    s = {x["id"]: x for x in _plan()["slices"]}; fails = []
    for i, f in _frags().items():
        for h in f.get("H", []):
            t = s.get(h)
            if not t or not (t["wt"] == "CON" or t["scope"] == s.get(i, {}).get("scope")):
                fails.append(f"{i}: H dependency {h} is not same-service or a contract")
        if f.get("I") and f.get("wt") != "ITG":
            fails.append(f"{i}: I dependencies allowed only on ITG stories")
    return _res(fails)

def c07(files=None):
    import networkx as nx
    s = {x["id"]: x for x in _plan()["slices"]}; g = nx.DiGraph()
    for i, f in _frags().items():
        if f.get("wt") != "CON":
            g.add_node(i)
            for h in f.get("H", []):
                if s.get(h, {}).get("wt") != "CON":
                    g.add_edge(h, i)
    if not nx.is_directed_acyclic_graph(g):
        return _res(["dependency cycle in fragments"])
    return _res([f"lane deeper than 4: {' -> '.join(p)}" for c in nx.weakly_connected_components(g)
                 for p in [nx.dag_longest_path(g.subgraph(c))] if len(p) > 4])

def c08(files=None):
    teams = {f.get("owner") for f in _frags().values() if f.get("ready") == "Day 1"}
    return _res([f"no Day-1 story for team type {t}" for t in ("TechX", "ACE", "INFRA", "DEVOPS", "QA") if t not in teams])

def c09(files=None):
    plan = _plan(); fails = []
    for k, v in plan["legacy"].items():
        if v["disposition"] in ("Retired (D-RCV-53)", "Already retired"):
            continue
        if not v["slices"]:
            fails.append(f"{k}: no new story")
    idx = {r["key"]: r for r in read_json(WORK / "plan" / "legacy_index.json", [])}
    for x in plan["slices"]:
        if x.get("preserved") and (ROOT / x["file"]).exists():
            t = _t(ROOT / x["file"])
            if "As built (monolith)" not in t:
                fails.append(f"{x['id']}: preserved story lacks the 'As built (monolith)' heading")
    return _res(fails)

def c10(files=None):
    plan = _plan(); idx = {r["key"]: r for r in read_json(WORK / "plan" / "legacy_index.json", [])}
    owned = {}
    for f in _frags().values():
        for a in f.get("acs", []):
            owned.setdefault(f.get("legacy"), set()).add(a.get("id") if isinstance(a, dict) else a)
    fails = []
    for k, v in plan["legacy"].items():
        if v["disposition"] in ("Retired (D-RCV-53)", "Already retired") or k not in idx:
            continue
        miss = [a for a in idx[k]["acs"] if a not in owned.get(k, set())]
        if miss:
            fails.append(f"{k}: legacy ACs not owned by any new story: {miss}")
    return _res(fails)

def c11(files=None):
    idx = read_json(WORK / "plan" / "legacy_index.json", []); plan = _plan()
    seen = set()
    for x in plan["slices"]:
        p = ROOT / x["file"]
        if p.exists():
            seen.update(re.findall(r"\bTC-[A-Z0-9]+-\d{3}-\d{2}\b", _t(p)))
    fails = [f"{r['key']}: legacy TC {t} not in any new story" for r in idx
             if plan["legacy"].get(r["key"], {}).get("disposition", "").startswith(("Retired", "Already")) is False for t in r["tcs"] if t not in seen]
    return _res(fails, warn=True)

def _names():
    names = set()
    for p in ROOT.glob("21*/**/*"):
        if p.suffix.lower() == ".csv":
            with open(p, encoding="utf-8", errors="ignore", newline="") as f:
                for row in csv.DictReader(f):
                    for k, v in row.items():
                        if k and re.search(r"(?i)assignee|reporter|creator|watcher|author|updated by", k) and v and " " in v.strip():
                            names.add(v.strip().lower())
        elif p.suffix.lower() == ".json":
            try:
                txt = p.read_text(encoding="utf-8", errors="ignore")
            except OSError:
                continue
            names.update(n.lower() for n in re.findall(r'"displayName"\s*:\s*"([^"@]+ [^"@]+)"', txt))
    return names

def c12(files, names=None):
    names = _names() if names is None else names; fails = []
    email = re.compile(r"\b[\w.+-]+@[\w-]+\.[\w.]+\b")
    for p in files:
        p = Path(p)
        if p.suffix.lower() not in (".md", ".json", ".yaml", ".sql", ".txt") or not p.exists():
            continue
        for n, line in enumerate(_t(p).splitlines(), 1):
            low = line.lower()
            if any(nm in low for nm in names):
                fails.append(f"{p.name}:{n}: person name from the deny-list")
            if email.search(line) and "example" not in low and "noreply" not in low:
                fails.append(f"{p.name}:{n}: email address")
    return _res(fails)

def c13(files):
    fails = []
    for p in files:
        p = Path(p)
        if p.name in JIRA_OK or p.suffix.lower() not in (".md", ".json", ".yaml", ".txt") or not p.exists():
            continue
        t = _t(p)
        if re.search(r"(?i)\bjira\b|atlassian\.net", t):
            preserved = "As built (monolith)" in t
            fails.append(f"{p.name}: refers to the issue tracker" + (" (inside a word-for-word preserved copy)" if preserved else ""))
    return _res(fails)

def c14(files):
    fails = []
    for p in files:
        p = Path(p)
        if p.suffix == ".md" and p.exists() and not p.name.startswith("RWB ") and "_work" not in p.parts:
            head = "\n".join(_t(p).splitlines()[:6])
            if "SCB Collections and Recovery. Henka Group," not in head:
                fails.append(f"{p.name}: header lines (Template and Rules §R8.1) missing")
    return _res(fails)

def c15(files=None):
    s = {x["id"]: x for x in _plan()["slices"]}; fails = []
    for i, f in _frags().items():
        rel = s.get(i, {}).get("release", "")
        if rel and rel not in str(f.get("release", "")):
            fails.append(f"{i}: release date changed ({f.get('release')} vs {rel})")
        p = ROOT / s.get(i, {}).get("file", "")
        if rel and p.exists() and "(tentative)" not in _t(p):
            fails.append(f"{i}: release not marked (tentative)")
    return _res(fails)

def c16(files):
    fails = []
    for p in _stories(files):
        t = _t(p)
        for rx, grp in [(r"\brwb\.([a-z-]+)\.events\.v1\b", 1), (r"/api/recovery/([a-z-]+)/v1\b", 1), (r"\bqueue rwb-([a-z-]+)\b", 1)]:
            for m in re.finditer(rx, t):
                if m.group(grp) not in SHORTS:
                    fails.append(f"{p.name}: unknown service name '{m.group(grp)}' in {m.group(0)}")
        if re.search(r"/api/recovery/v1/", t) and "As built (monolith)" not in t:
            fails.append(f"{p.name}: old monolith API base outside the as-built section")
    return _res(fails)

def c17(files=None):
    req_g = {"id", "title", "description", "type", "severity"}; req_a = {"id", "text", "why"}
    ids, fails = set(), []
    for kind, req in (("gaps", req_g), ("assumptions", req_a)):
        for p in (WORK / kind).glob("*.jsonl"):
            for r in read_jsonl(p):
                miss = req - set(k for k, v in r.items() if v not in (None, ""))
                if miss:
                    fails.append(f"{p.name}: {r.get('id')} missing {sorted(miss)}")
                ids.add(r.get("id"))
    cite = re.compile(r"\b(?:CG|ASM)-[A-Za-z0-9]+(?:-[A-Za-z0-9]+)*-\d+\b")
    for p in files or []:
        p = Path(p)
        if p.suffix in (".md", ".json") and p.exists():
            for c in set(cite.findall(_t(p))):
                if c not in ids:
                    fails.append(f"{p.name}: cites {c} but no jsonl row has that id")
    return _res(fails)

def _wp_writes(wp):
    t = _t(WORK / "wp" / f"{wp}.md")
    blk = t.split("Write only:", 1)[1].split("\nDo", 1)[0] if "Write only:" in t else ""
    return [l[2:].split(" (")[0].strip() for l in blk.splitlines() if l.startswith("- ")]

def c18(files, wp=None):
    if not wp:
        return ("PASS", [])
    allowed = _wp_writes(wp); log = WORK / "editlog" / f"{wp}.md"; fails = []
    if log.exists():
        for m in re.findall(r"(?m)^\s*[-*]\s+`?([^`\n]+?\.(?:md|json|jsonl|xlsx|docx|pptx|yaml|sql|svg|excalidraw))`?\s*$", _t(log)):
            if not any(m.replace("\\", "/").startswith(a.rstrip("/")) for a in allowed):
                fails.append(f"{wp}: wrote outside 'Write only': {m}")
    masters = read_json(WORK / "plan" / "legacy_hashes.json", {}) or {}
    for k, h in masters.items():
        p = ROOT / "04 User stories" / k if not k.startswith("04 ") else ROOT / k
        if p.exists() and sha256(p) != h:
            fails.append(f"legacy file changed: {k}")
    return _res(fails)

def c19(files=None):
    fails = []
    for q in sorted((WORK / "wp").glob("queue-*.json")):
        for item in json.loads(q.read_text(encoding="utf-8")):
            for e in item.get("expect", []):
                p = ROOT / e
                if not p.exists():
                    fails.append(f"{item['wp']}: planned output missing: {e}")
                elif p.suffix == ".md" and "editlog" not in e and "fragments" not in e and "D-RCV-53" not in _t(p):
                    fails.append(f"{item['wp']}: {p.name} has no D-RCV-53 change-log row")
    return _res(fails)

def c20(files=None):
    fails = []
    for p in (WORK / "editlog").glob("*.md"):
        if TOOL not in _t(p):
            fails.append(f"{p.name}: tool line missing")
    for p in files or []:
        p = Path(p)
        if p.suffix in (".md", ".json") and p.exists() and re.search(r"Co-Authored-By: Claude|Generated with \[Claude Code\]", _t(p)):
            fails.append(f"{p.name}: wrong tool attribution")
    return _res(fails)

ALL = {f"C{n:02d}": globals()[f"c{n:02d}"] for n in range(1, 21)}

def outputs(stage=None):
    files = []
    for q in sorted((WORK / "wp").glob("queue-*.json")):
        if stage and q.stem != f"queue-{stage}":
            continue
        for item in json.loads(q.read_text(encoding="utf-8")):
            for e in item.get("expect", []):
                p = ROOT / e
                files += [f for f in p.rglob("*") if f.is_file()] if p.is_dir() else ([p] if p.exists() else [])
    if stage in (None, "B"):
        files += [ROOT / x["file"] for x in _plan()["slices"] if (ROOT / x["file"]).exists()]
    return sorted(set(files))

def main():
    ap = argparse.ArgumentParser(); ap.add_argument("--wp"); ap.add_argument("--quick", action="store_true")
    ap.add_argument("--stage", choices=["B", "C", "D"]); ap.add_argument("--full", action="store_true"); a = ap.parse_args()
    if a.wp:
        files = [ROOT / w for w in _wp_writes(a.wp)]
        files = [f for p in files for f in ([x for x in p.rglob("*") if x.is_file()] if p.is_dir() else [p]) if f.exists()]
        names, mode = QUICK, f"wp-{a.wp}"
    elif a.stage:
        files, names, mode = outputs(a.stage), STAGES[a.stage], f"stage-{a.stage}"
    else:
        files, names, mode = outputs(), list(ALL), "full"
    res = {}
    for n in names:
        try:
            res[n] = ALL[n](files, wp=a.wp) if n == "C18" else ALL[n](files)
        except Exception as e:
            res[n] = ("FAIL", [f"check crashed: {type(e).__name__}: {e}"])
    ts = time.strftime("%Y%m%d-%H%M%S"); rep = R22 / "checks" / "reports"; rep.mkdir(parents=True, exist_ok=True)
    lines = [f"# Check report {mode} {ts}\n", "| Check | Result | Findings |", "|---|---|---|"]
    lines += [f"| {n} | {r[0]} | {len(r[1])} |" for n, r in res.items()]
    for n, r in res.items():
        if r[1]:
            lines += [f"\n## {n} {r[0]}\n"] + [f"- {x}" for x in r[1]]
    (rep / f"{mode}-{ts}.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
    (rep / f"{mode}-{ts}.json").write_text(json.dumps({n: {"result": r[0], "findings": r[1]} for n, r in res.items()}, indent=1), encoding="utf-8")
    for n, r in res.items():
        print(n, r[0], len(r[1]))
    sys.exit(1 if any(r[0] == "FAIL" for r in res.values()) else 0)

if __name__ == "__main__":
    main()
```

- [ ] **Step 4: Run the tests and a dry full run.** The full run is expected to FAIL now (no stories yet). It proves only that the script runs end to end.

```powershell
python -I "22 Microservice Realignment/checks/run_all.py" --full
```

Expected:
- All unit tests OK.
- The dry run prints 20 lines `Cnn PASS|WARN|FAIL n`, with C01 `PASS` and C04 and C19 `FAIL`.
- A report is written to `checks/reports/full-*.md`.

If C01 FAILs at this point, an earlier task wrote into a read-only area. Find the file in the report and restore it from git (`git checkout -- "<file>"` for a tracked file) before continuing.

---

### Task 17: Update the AI-SDLC workspace context (step A10)

**Files:**
- Output: `22 Microservice Realignment/aisdlc/.github/contexts/realignment-v5-context.md`. The context-updater agent writes this file inside the workspace copy only.

- [ ] **Step 1: Run queue A10.**

```powershell
python -I "22 Microservice Realignment/compat/run_parallel.py" --queue A10
```

Expected: `RESULT {"DONE": 1}`. The BRD and PRD builders read the new context file in Stage B.

If the run fails after its retry, write the context file yourself from the two Text Extract files:
1. Put a 1-page summary in it: the 19 services, the waves, the naming rules and "no data lake".
2. Record an ASM.
3. Continue.

---

### Task 18: Excalidraw diagram builder (epic, master and wave diagrams)

**Files:**
- Create: `22 Microservice Realignment/compat/build_arch_diagram.py`
- Test: `22 Microservice Realignment/compat/tests/test_diagram.py`
- Output:
  - `--epics` (Task 20): `16 Story diagrams/Recovery Workbench Service Epic Diagrams v1/<epic>.excalidraw` and `.svg`, 31 pairs.
  - `--master` (Task 21): in `22 Microservice Realignment/`:
    - `Recovery Workbench Microservice Architecture by Epic and Story v1.excalidraw` and `.svg`
    - `Recovery Workbench Wave <1-4> Architecture v1.excalidraw` and `.svg`

**Layout:**
- Horizontal bands for Wave 0 (platform) to Wave 4, with integration last.
- Inside each band, one epic frame per epic.
- Inside each frame, one box per story, grouped in columns by lane.

**Styles** (Appendix R §R8.8):

| Item | Style |
|---|---|
| CON | blue `#1971c2` |
| APP | green `#2f9e44` |
| DB | brown `#8d5524` |
| INF | grey `#868e96` |
| OPS | purple `#7048e8` |
| ITG | red `#e03131` |
| Build dependency (H) | thin black arrows inside a frame |
| REST call between epics | solid blue arrow |
| Kafka call between epics | dashed orange arrow |
| Temporal call between epics | purple arrow |
| File call between epics | dotted grey arrow |

- [ ] **Step 1: Write the failing test.**

```python
import json, tempfile, unittest
from pathlib import Path
import build_arch_diagram as bd

S = [{"id": "RWB-P3-E1018-CON", "title": "Case contract", "wt": "CON", "epic": "RWB-SVC-P3", "lane": "CG-W1", "wave": 1, "scope": "P3", "H": [], "C": [], "I": []},
     {"id": "RWB-P3-E1018-APP", "title": "Case app", "wt": "APP", "epic": "RWB-SVC-P3", "lane": "L-P3-A", "wave": 1, "scope": "P3", "H": ["RWB-P3-E1018-CON"], "C": ["RWB-P1-E1016-CON"], "I": []},
     {"id": "RWB-P1-E1016-CON", "title": "Source contract", "wt": "CON", "epic": "RWB-SVC-P1", "lane": "CG-W1", "wave": 1, "scope": "P1", "H": [], "C": [], "I": []}]
F = {"RWB-P3-E1018-APP": {"events_consumed": ["rwb.source-data.AccountLoaded.v1"], "ops_consumed": [], "workflows": []}}

class TestDiagram(unittest.TestCase):
    def test_build(self):
        doc = bd.build(S, F, title="T")
        els = doc["elements"]; ids = {e["id"] for e in els}
        boxes = [e for e in els if e["type"] == "rectangle" and e.get("customData", {}).get("story")]
        self.assertEqual(len(boxes), 3)
        for e in els:
            if e["type"] == "arrow":
                self.assertIn(e["startBinding"]["elementId"], ids); self.assertIn(e["endBinding"]["elementId"], ids)
        kinds = {e.get("customData", {}).get("call") for e in els if e["type"] == "arrow"}
        self.assertTrue({"H", "REST", "Kafka"} <= kinds, kinds)
        with tempfile.TemporaryDirectory() as d:
            bd.save(doc, Path(d) / "x")
            self.assertEqual(json.loads((Path(d) / "x.excalidraw").read_text(encoding="utf-8"))["type"], "excalidraw")
            self.assertTrue((Path(d) / "x.svg").read_text(encoding="utf-8").startswith("<svg"))
```

- [ ] **Step 2: Run the tests.** Expected: FAIL (import error).

- [ ] **Step 3: Write `build_arch_diagram.py`.**

```python
"""Excalidraw v2 diagrams by epic and story, plus an SVG render of the same elements. Deterministic layout."""
import argparse, hashlib, html, json, sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
from common import ROOT, R22, WORK, SERVICES, read_json, write_json

COL = {"CON": "#1971c2", "APP": "#2f9e44", "DB": "#8d5524", "INF": "#868e96", "OPS": "#7048e8", "ITG": "#e03131"}
CALL = {"H": ("#000000", "solid", 1), "REST": ("#1971c2", "solid", 2), "Kafka": ("#f08c00", "dashed", 2),
        "Temporal": ("#7048e8", "solid", 2), "File": ("#868e96", "dotted", 2), "I": ("#e03131", "dashed", 1)}
BW, BH, GX, GY, PAD = 220, 56, 24, 14, 24
SHORT2CODE = {s["short"]: s["code"] for s in SERVICES}

def _seed(s):
    return int(hashlib.md5(s.encode()).hexdigest()[:8], 16)

def _base(eid, typ, x, y, w, h, stroke="#1e1e1e", bg="transparent", style="solid", width=1, **kw):
    e = {"id": eid, "type": typ, "x": x, "y": y, "width": w, "height": h, "angle": 0, "strokeColor": stroke,
         "backgroundColor": bg, "fillStyle": "solid", "strokeWidth": width, "strokeStyle": style, "roughness": 0,
         "opacity": 100, "groupIds": [], "frameId": None, "roundness": None, "seed": _seed(eid), "version": 1,
         "versionNonce": _seed(eid + "n"), "isDeleted": False, "boundElements": [], "updated": 1, "link": None, "locked": False}
    e.update(kw); return e

def _text(eid, x, y, w, h, txt, size=14, container=None, color="#1e1e1e"):
    return _base(eid, "text", x, y, w, h, stroke=color, text=txt, originalText=txt, fontSize=size, fontFamily=2,
                 textAlign="center" if container else "left", verticalAlign="middle" if container else "top",
                 containerId=container, lineHeight=1.25, autoResize=True)

def _box(eid, x, y, w, h, label, color, story=None, size=12):
    r = _base(eid, "rectangle", x, y, w, h, stroke=color, bg=color + "22", width=2, roundness={"type": 3},
              customData={"story": story} if story else {})
    t = _text(eid + "-t", x + 4, y + 4, w - 8, h - 8, label, size=size, container=eid)
    r["boundElements"] = [{"id": t["id"], "type": "text"}]
    return [r, t]

def _arrow(eid, a, b, kind):
    c, st, w = CALL[kind]
    x1, y1 = a["x"] + a["width"], a["y"] + a["height"] / 2; x2, y2 = b["x"], b["y"] + b["height"] / 2
    if x2 < x1:
        x1, x2 = a["x"], b["x"] + b["width"]
    e = _base(eid, "arrow", x1, y1, x2 - x1, y2 - y1, stroke=c, style=st, width=w, points=[[0, 0], [x2 - x1, y2 - y1]],
              lastCommittedPoint=None, startBinding={"elementId": a["id"], "focus": 0, "gap": 4},
              endBinding={"elementId": b["id"], "focus": 0, "gap": 4}, startArrowhead=None, endArrowhead="arrow",
              customData={"call": kind})
    a["boundElements"].append({"id": eid, "type": "arrow"}); b["boundElements"].append({"id": eid, "type": "arrow"})
    return e

def _band(x):
    return 9 if str(x["epic"]).startswith("RWB-ITG") else (0 if str(x["epic"]).startswith("RWB-PLT") else x["wave"])

def _owner_of(name, own_events):
    if name in own_events:
        return own_events[name].get("owner")
    parts = str(name).split(".")
    return SHORT2CODE.get(parts[1]) if len(parts) > 2 and parts[0] == "rwb" else None

def build(slices, frags, title, own=None):
    own = own or {}; els = []; story_el = {}; frame_el = {}
    y = 80
    els.append(_text("title", 40, 20, 1600, 40, title, size=28))
    for band in sorted({_band(x) for x in slices}):
        bx = 40; in_band = [x for x in slices if _band(x) == band]
        label = {0: "Wave 0 - platform", 9: "Integration"}.get(band, f"Wave {band}")
        els.append(_text(f"band-{band}", 40, y, 600, 30, label, size=22)); y += 40; row_h = 0
        for epic in sorted({x["epic"] for x in in_band}):
            ss = [x for x in in_band if x["epic"] == epic]
            lanes = sorted({x.get("lane") or "?" for x in ss}, key=lambda l: (not l.startswith("CG"), l))
            cols = {l: [x for x in ss if (x.get("lane") or "?") == l] for l in lanes}
            w = PAD * 2 + len(lanes) * (BW + GX) - GX; h = PAD * 2 + 30 + max(len(v) for v in cols.values()) * (BH + GY)
            fr = _base(f"frame-{epic}", "rectangle", bx, y, w, h, stroke="#343a40", width=2, customData={"epic": epic})
            els += [fr, _text(f"frame-{epic}-t", bx + PAD, y + 6, w - 2 * PAD, 24, epic, size=16)]; frame_el[epic] = fr
            for ci, l in enumerate(lanes):
                for ri, x in enumerate(sorted(cols[l], key=lambda s: s["id"])):
                    sx = bx + PAD + ci * (BW + GX); sy = y + PAD + 30 + ri * (BH + GY)
                    pair = _box(f"s-{x['id']}", sx, sy, BW, BH, f"{x['id']}\n{x['title'][:34]}", COL[x["wt"]], story=x["id"])
                    els += pair; story_el[x["id"]] = pair[0]
            bx += w + 60; row_h = max(row_h, h)
            if bx > 9000:
                bx = 40; y += row_h + 60; row_h = 0
        y += row_h + 80
    n = 0; seen = set()
    def add(a, b, kind):
        nonlocal n
        key = (a["id"], b["id"], kind)
        if a is b or key in seen:
            return
        seen.add(key); n += 1; els.append(_arrow(f"a{n}-{kind}", a, b, kind))
    by_code = {}
    for x in slices:
        by_code.setdefault(x["scope"], x["epic"])
    for x in slices:
        me = story_el.get(x["id"])
        for h in x.get("H", []):
            if h in story_el and slices_epic(slices, h) == x["epic"]:
                add(story_el[h], me, "H")
        for c in x.get("C", []):
            if c in story_el:
                add(me, story_el[c], "REST")
        for i in x.get("I", []):
            if i in story_el:
                add(me, story_el[i], "I")
        f = frags.get(x["id"], {})
        for ev in f.get("events_consumed", []) or []:
            o = _owner_of(ev, own.get("events", {}))
            if o in by_code and by_code[o] in frame_el:
                add(frame_el[by_code[o]], me, "Kafka")
        for op in f.get("ops_consumed", []) or []:
            o = (own.get("api", {}).get(op) or {}).get("owner")
            if o in by_code and by_code[o] in frame_el:
                add(me, frame_el[by_code[o]], "REST")
        for wf in f.get("workflows", []) or []:
            o = (own.get("workflows", {}).get(wf) or {}).get("owner")
            if o in by_code and o != x["scope"] and by_code[o] in frame_el:
                add(me, frame_el[by_code[o]], "Temporal")
        if any(k in x["title"] for k in ("MFT", "SFTP", "file")) and "P2" in by_code and x["scope"] != "P2":
            add(me, frame_el[by_code["P2"]], "File")
    lx = 40; ly = y + 20
    els.append(_text("legend-t", lx, ly, 300, 24, "Legend", size=18))
    for i, (k, c) in enumerate(COL.items()):
        els += _box(f"legend-{k}", lx + i * 130, ly + 30, 120, 36, k, c)
    for i, (k, (c, st, w)) in enumerate(CALL.items()):
        a = _base(f"legend-a-{k}", "line", lx + i * 160, ly + 90, 80, 0, stroke=c, style=st, width=w, points=[[0, 0], [80, 0]])
        els += [a, _text(f"legend-at-{k}", lx + i * 160 + 86, ly + 80, 70, 20, k, size=12)]
    return {"type": "excalidraw", "version": 2, "source": "https://excalidraw.com", "elements": els,
            "appState": {"viewBackgroundColor": "#ffffff", "gridSize": None}, "files": {}}

def slices_epic(slices, sid, _cache={}):
    if not _cache or sid not in _cache:
        _cache.clear(); _cache.update({x["id"]: x["epic"] for x in slices})
    return _cache.get(sid)

def svg(doc):
    els = doc["elements"]
    W = max(e["x"] + max(e["width"], 0) for e in els) + 40; H = max(e["y"] + max(e["height"], 0) for e in els) + 40
    out = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{int(W)}" height="{int(H)}" viewBox="0 0 {int(W)} {int(H)}" font-family="Helvetica, Arial">',
           '<defs><marker id="ah" markerWidth="8" markerHeight="8" refX="8" refY="4" orient="auto"><path d="M0,0 L8,4 L0,8 z" fill="context-stroke"/></marker></defs>',
           f'<rect width="{int(W)}" height="{int(H)}" fill="#ffffff"/>']
    dash = {"solid": "", "dashed": ' stroke-dasharray="8 6"', "dotted": ' stroke-dasharray="2 4"'}
    for e in els:
        if e["type"] == "rectangle":
            fill = e["backgroundColor"] if e["backgroundColor"] != "transparent" else "none"
            out.append(f'<rect x="{e["x"]}" y="{e["y"]}" width="{e["width"]}" height="{e["height"]}" rx="6" fill="{fill[:7]}" fill-opacity="0.13" stroke="{e["strokeColor"]}" stroke-width="{e["strokeWidth"]}"/>')
        elif e["type"] in ("arrow", "line"):
            p = e["points"][-1]; mk = ' marker-end="url(#ah)"' if e["type"] == "arrow" else ""
            out.append(f'<line x1="{e["x"]}" y1="{e["y"]}" x2="{e["x"] + p[0]}" y2="{e["y"] + p[1]}" stroke="{e["strokeColor"]}" stroke-width="{e["strokeWidth"]}"{dash[e["strokeStyle"]]}{mk}/>')
        elif e["type"] == "text":
            lines = e["text"].split("\n"); cx = e["x"] + e["width"] / 2 if e.get("containerId") else e["x"]
            anchor = "middle" if e.get("containerId") else "start"
            for i, l in enumerate(lines):
                yy = e["y"] + e["fontSize"] * (1.1 + i * 1.25)
                out.append(f'<text x="{cx}" y="{yy}" font-size="{e["fontSize"]}" text-anchor="{anchor}" fill="{e["strokeColor"]}">{html.escape(l)}</text>')
    out.append("</svg>")
    return "\n".join(out)

def save(doc, stem):
    stem = Path(stem); stem.parent.mkdir(parents=True, exist_ok=True)
    for ext, body in ((".excalidraw", json.dumps(doc, indent=1)), (".svg", svg(doc))):
        p = stem.with_name(stem.name + ext)
        if p.exists() and p.read_text(encoding="utf-8") != body and "v1" in stem.name and (WORK / "plan" / "diagram_written.json").exists() is False:
            raise SystemExit(f"REFUSED: {p} exists")
        p.write_text(body, encoding="utf-8")
    print("WROTE", stem.name)

def _load():
    plan = read_json(WORK / "plan" / "split_plan.json")
    frags = {p.stem: json.loads(p.read_text(encoding="utf-8")) for p in (WORK / "fragments").glob("*.json")}
    return plan["slices"], frags, read_json(WORK / "plan" / "ownership.json", {}) or {}

if __name__ == "__main__":
    ap = argparse.ArgumentParser(); g = ap.add_mutually_exclusive_group(required=True)
    g.add_argument("--epics", action="store_true"); g.add_argument("--master", action="store_true"); a = ap.parse_args()
    slices, frags, own = _load()
    if a.epics:
        d = ROOT / "16 Story diagrams" / "Recovery Workbench Service Epic Diagrams v1"
        for epic in sorted({x["epic"] for x in slices}):
            ss = [x for x in slices if x["epic"] == epic]
            ids = {x["id"] for x in ss} | {c for x in ss for c in x["C"] + x["I"]}
            save(build([x for x in slices if x["id"] in ids], frags, f"{epic} - stories, lanes and contracts (D-RCV-53)", own), d / epic)
    else:
        save(build(slices, frags, "Recovery Workbench microservice architecture by epic and story v1 (D-RCV-53)", own),
             R22 / "Recovery Workbench Microservice Architecture by Epic and Story v1")
        for w in (1, 2, 3, 4):
            ss = [x for x in slices if x["wave"] == w or (x["wave"] == 0 and w == 1)]
            save(build(ss, frags, f"Recovery Workbench Wave {w} architecture v1 (D-RCV-53)", own), R22 / f"Recovery Workbench Wave {w} Architecture v1")
    write_json(WORK / "plan" / "diagram_written.json", {"done": True})
```

- [ ] **Step 4: Run the tests.** Expected: OK. The diagrams themselves are built in Tasks 20 and 21, once the fragments exist.

---

## 4. Tasks — Stages B, C and D (maximum parallel fan-out)

### Task 19: Stage B — all story, requirement, architecture and document WPs at once

**Files:**
- Input: `_work/msr/wp/queue-B.json` (Task 13)
- Output: every file under "Write only" in every B WP, plus `_work/msr/fragments/*.json`, `_work/msr/gaps/*.jsonl`, `_work/msr/assumptions/*.jsonl` and `_work/msr/editlog/*.md`

Every WP in queue B is independent:
- Each story file belongs to exactly one WP.
- Each document family belongs to exactly one WP.
- Every WP writes its own jsonl and edit-log files.

So there is no ordering inside Stage B. The runner fills the measured budget from the first second.

- [ ] **Step 1: Start Stage B at the measured budget.**

```powershell
python -I "22 Microservice Realignment/compat/run_parallel.py" --queue B
```

Expected:
- First line: `RUN queue=queue-B.json items=<n> budget=<capacity budget> fanout=<capacity fanout>`.
- Last line: `RESULT {"DONE": <n>}`.

**Exit code 3 (PAUSED_QUOTA):** the OpenCode Go weekly or monthly window is at 95 % or more. Rerun the same command after the `resetsAt` time shown in `_work/msr/status.json`. DONE WPs are skipped.

- [ ] **Step 2: Rerun until no WP is FAILED.** The runner retries every WP that is not DONE, so run the same command again:

```powershell
python -I "22 Microservice Realignment/compat/run_parallel.py" --queue B
```

If a WP is FAILED twice in a row:
1. Open `_work/msr/logs/<WP>.log`.
2. Fix the cause (usually a path in the WP file).
3. Rerun only that WP:

```powershell
python -I "22 Microservice Realignment/compat/run_parallel.py" --queue B --only <WP>
```

Never split, lower or serialise the queue to work around a failure.

- [ ] **Step 3: Run the stage checks and fix the findings.**

```powershell
python -I "22 Microservice Realignment/checks/run_all.py" --stage B
```

Expected: no FAIL. C11 and C13 may WARN inside preserved copies.

For each FAIL finding:
1. Note the WP whose output is named (the story file → its WP in `queue-B.json`).
2. Requeue those WPs:

```powershell
python -I "22 Microservice Realignment/compat/requeue.py" <WP1>,<WP2>
```

3. Rerun Step 2.

Write `requeue.py` now. It removes the listed WPs from `status.json` so the runner runs them again:

```python
# 22 Microservice Realignment/compat/requeue.py
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
from common import WORK, read_json, write_json

st = read_json(WORK / "status.json", {}) or {}
for wp in sys.argv[1].split(","):
    st.pop(wp.strip(), None)
    print("REQUEUED", wp.strip())
write_json(WORK / "status.json", st)
```

A requeued story WP rewrites its own files. These are new files of this run, never baseline files, so this is allowed by AGENTS.md rule 1.

---

### Task 20: Stage C — assemble masters and the catalogue, then cross-cutting WPs, then the epic diagrams

**Files:**
- Create: `22 Microservice Realignment/compat/assemble.py`
- Test: `22 Microservice Realignment/compat/tests/test_assemble.py`
- Output:
  - **Next versions of the 7 masters in `04 User stories/`:**
    - Epic 1 v10
    - Epic 2 v8
    - Epics 3 to 8 v4
    - Technical Enabler v8
    - Administration v4
    - Data Migration v4
    - ACE Team v2
  - **New files in `04 User stories/`:**
    - `Recovery Workbench Service Story Catalog v1.xlsx`
    - one `<epic> Epic Overview v1.md` per epic folder in `Recovery Workbench Service Story Files v1/`
  - **New file in `11 Delivery and operations/`:** `Recovery Workbench Day-1 Work Allocation v1.xlsx`
  - **PRD references:** written into the story files and fragments created by this run.

- [ ] **Step 1: Write the failing test.**

```python
import unittest
import assemble as asm

class TestAssemble(unittest.TestCase):
    def test_prd_ref_and_demote(self):
        prd = "| FR-P3-001 | Open a case | REQ-CAS-001, REQ-CAS-002 |\n| FR-P3-002 | Close | REQ-CAS-009 |\n"
        m = asm.fr_map(prd)
        self.assertEqual(m["REQ-CAS-002"], ["FR-P3-001"])
        self.assertEqual(asm.prd_value("03/PRD/x.md", ["REQ-CAS-001", "REQ-CAS-009"], m), "03/PRD/x.md (FR-P3-001, FR-P3-002)")
        self.assertTrue(asm.prd_value("03/PRD/x.md", ["REQ-ZZZ-001"], m).startswith("03/PRD/x.md (no FR mapped"))
        self.assertEqual(asm.demote("# A\n### 1. Story\n"), "### A\n##### 1. Story\n")
```

- [ ] **Step 2: Run the tests.** Expected: FAIL (import error).

- [ ] **Step 3: Write `assemble.py`.**

```python
"""Stage C assembler: the only writer of master files (AGENTS.md rule 7)."""
import collections, json, re, sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
from common import ROOT, WORK, STORIES, SERVICES, OWNER, WT_NAME, header, next_version, read_json, write_json, add_gap, reset_cands
from xlsx_write import write_book
import legacy_index as li
from split_plan import EPIC_NAMES, OUT_DIR

TOOL = "Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash. Decision D-RCV-53."
F3 = "03 Requirements and specifications"

def fr_map(prd_text):
    m = {}
    for line in prd_text.splitlines():
        fr = re.findall(r"\bFR-(?:P10|P[1-9]|S[1-9]|PLT)-\d{3}\b", line)
        if fr:
            for r in re.findall(r"\bREQ-[A-Z]+-\d{3}\b", line):
                m.setdefault(r, [])
                for f in fr:
                    if f not in m[r]:
                        m[r].append(f)
    return m

def prd_value(path, reqs, m):
    frs = sorted({f for r in reqs for f in m.get(r, [])})
    return f"{path} ({', '.join(frs)})" if frs else f"{path} (no FR mapped to {', '.join(reqs) or 'no REQ IDs'})"

def demote(t):
    return re.sub(r"(?m)^(#{1,4}) ", lambda x: "#" * (len(x.group(1)) + 2) + " ", t)

def _prd_path(scope):
    s = next((x for x in SERVICES if x["code"] == scope), None)
    name = f"Recovery Workbench PRD {s['code']} {s['service']} v1.md" if s else "Recovery Workbench PRD PLT Platform v1.md"
    return f"{F3}/PRD/{name}"

def prd_refs(plan):
    reset_cands("C1"); cache = {}; done = 0
    for x in plan["slices"]:
        rel = _prd_path(x["scope"] if x["scope"] != "ITG" else "PLT")
        if rel not in cache:
            p = ROOT / rel
            cache[rel] = fr_map(p.read_text(encoding="utf-8", errors="replace")) if p.exists() else None
        m = cache[rel]
        if m is None:
            val = f"Not specified in the source documents ({add_gap('C1', f'PRD missing: {rel}', 'PRD WP did not produce the file', severity='P2', area='Requirements')})"
        else:
            val = prd_value(rel, x.get("reqs", []), m)
        sp = ROOT / x["file"]; fp = WORK / "fragments" / f"{x['id']}.json"
        if sp.exists():
            t = sp.read_text(encoding="utf-8")
            nt = re.sub(r"(?m)^\|\s*PRD reference\s*\|[^\n]*\|\s*$", f"| PRD reference | {val} |", t, count=1)
            if nt != t:
                sp.write_text(nt, encoding="utf-8"); done += 1
        if fp.exists():
            f = json.loads(fp.read_text(encoding="utf-8")); f["prd_ref"] = val; write_json(fp, f)
    print("C1 PRD references written:", done)

MASTER_STEMS = [("Recovery Workbench User Stories Epic 1", "E1"), ("Recovery Workbench User Stories Epic 2", "E2"),
                ("Recovery Workbench User Stories Epics 3 to 8", "E3-8"), ("Recovery Workbench Technical Enabler Stories", "TE"),
                ("Recovery Workbench Administration Stories", "AD"), ("Recovery Workbench Data Migration Stories", "DM"),
                ("Recovery Workbench ACE Team Stories", "ACE")]

def masters(plan, idx):
    s = {x["id"]: x for x in plan["slices"]}
    for stem, grp in MASTER_STEMS:
        n = next_version(STORIES, stem); out = STORIES / f"{stem} v{n}.md"
        if out.exists():
            print("KEPT", out.name); continue
        t = [f"# {stem} v{n}\n", header(), TOOL,
             f"\nRealigned to the 19-service architecture (Arch v5). Each legacy story below lists its new linked stories; the full text of each new story follows. Release dates are tentative and unchanged.\n"]
        for r in [r for r in idx if r["group"] == grp]:
            lg = plan["legacy"].get(r["key"], {"disposition": "Not found", "slices": []})
            t += [f"\n## {r['key']} {r['title']}\n", f"Legacy disposition: {lg['disposition']}.\n",
                  "| New story | Work type | Service epic | Lane | Ready to start | Suggested owner |", "|---|---|---|---|---|---|"]
            for sid in lg["slices"]:
                x = s[sid]
                t.append(f"| {sid} | {WT_NAME[x['wt']]} | {x['epic']} | {x.get('lane')} | {x['ready']} | {OWNER[x['owner']]} |")
            for sid in lg["slices"]:
                p = ROOT / s[sid]["file"]
                t.append("\n" + (demote(p.read_text(encoding="utf-8")) if p.exists() else f"### {sid}\n\nNot written (see the Tracker WP status).\n"))
        out.write_text("\n".join(t) + "\n", encoding="utf-8"); print("WROTE", out.name)

def catalogue(plan, frags):
    epics = collections.defaultdict(list)
    for x in plan["slices"]:
        epics[x["epic"]].append(x)
    deps = [[x["id"], c, k] for x in plan["slices"] for k in ("H", "C", "I", "X") for c in x[k]]
    write_book(STORIES / "Recovery Workbench Service Story Catalog v1.xlsx", {
        "Epics": (["Epic", "Name", "Stories", "Lanes", "Day-1 stories", "Wave"],
                  [[e, EPIC_NAMES.get(e, e), len(v), len({x.get("lane") for x in v}), sum(1 for x in v if x["ready"] == "Day 1"), min(x["wave"] for x in v)] for e, v in sorted(epics.items())]),
        "Stories": (["Story", "Title", "Work type", "Suggested owner", "Service", "Epic", "Wave", "Business epic", "Release", "Legacy", "Disposition", "Lane", "Ready", "PRD", "File"],
                    [[x["id"], x["title"], WT_NAME[x["wt"]], OWNER[x["owner"]], x["service"], x["epic"], x["wave"], x["business_epic"],
                      (x["release"] + " (tentative)") if x["release"] else "", x["legacy"], x["disposition"], x.get("lane"), x["ready"],
                      frags.get(x["id"], {}).get("prd_ref", ""), x["file"]] for x in plan["slices"]]),
        "Legacy map": (["Legacy key", "Disposition", "New stories"], [[k, v["disposition"], v["slices"]] for k, v in sorted(plan["legacy"].items())]),
        "Dependencies": (["Story", "Depends on", "Class"], deps),
        "Contracts": (["Story", "Operations provided", "Operations consumed", "Events published", "Events consumed", "Workflows"],
                      [[i, f.get("ops_provided"), f.get("ops_consumed"), f.get("events_published"), f.get("events_consumed"), f.get("workflows")] for i, f in sorted(frags.items())]),
    }, read_me=header() + "\nRecovery Workbench Service Story Catalog v1. " + TOOL)
    print("WROTE Service Story Catalog v1.xlsx")

def overviews(plan):
    by = collections.defaultdict(list)
    for x in plan["slices"]:
        by[x["epic"]].append(x)
    for e, v in sorted(by.items()):
        p = ROOT / OUT_DIR / f"{e} {EPIC_NAMES[e]}" / f"{e} Epic Overview v1.md"
        if p.exists():
            continue
        p.parent.mkdir(parents=True, exist_ok=True)
        lanes = collections.defaultdict(list)
        for x in v:
            lanes[x.get("lane")].append(x)
        t = [f"# {e} {EPIC_NAMES[e]} - Epic Overview v1\n", header(), TOOL,
             f"\nWave {min(x['wave'] for x in v)}. Stories: {len(v)}. Ownership is suggested only; any team may pick up any story.\n",
             "## Suggested owners\n", "| Team type | Stories |", "|---|---|"]
        t += [f"| {OWNER[o]} | {n} |" for o, n in sorted(collections.Counter(x["owner"] for x in v).items())]
        t += ["\n## Day-1 stories\n"] + [f"- {x['id']} {x['title']}" for x in v if x["ready"] == "Day 1"]
        t += ["\n## Lanes\n", "| Lane | Stories | Ready to start |", "|---|---|---|"]
        t += [f"| {l} | {', '.join(x['id'] for x in xs)} | {'; '.join(sorted({x['ready'] for x in xs}))} |" for l, xs in sorted(lanes.items(), key=lambda kv: str(kv[0]))]
        p.write_text("\n".join(t) + "\n", encoding="utf-8")
    print("WROTE", len(by), "epic overviews")

def day1(plan):
    out = ROOT / "11 Delivery and operations" / "Recovery Workbench Day-1 Work Allocation v1.xlsx"
    sheets = {}
    for team in ("TechX", "ACE", "INFRA", "DEVOPS", "QA"):
        rows = [[x["id"], x["title"], WT_NAME[x["wt"]], x["epic"], x.get("lane"), x["file"]] for x in plan["slices"] if x["owner"] == team and x["ready"] == "Day 1"]
        sheets[team] = (["Story", "Title", "Work type", "Epic", "Lane", "File"], rows)
    write_book(out, sheets, read_me=header() + "\nDay-1 Work Allocation v1. Suggested owners by team type only; no names. " + TOOL)
    print("WROTE Day-1 Work Allocation v1.xlsx")

def main():
    plan = read_json(WORK / "plan" / "split_plan.json"); idx = read_json(WORK / "plan" / "legacy_index.json")
    prd_refs(plan)
    frags = {p.stem: json.loads(p.read_text(encoding="utf-8")) for p in (WORK / "fragments").glob("*.json")}
    masters(plan, idx); catalogue(plan, frags); overviews(plan); day1(plan)
    print("C OK")

if __name__ == "__main__":
    main()
```

- [ ] **Step 4: Run the tests, then the assembler.**

```powershell
python -I "22 Microservice Realignment/compat/assemble.py"
```

Expected:
- Tests OK.
- `C1 PRD references written: <n>`.
- Seven `WROTE … v<n>.md` lines.
- `WROTE Service Story Catalog v1.xlsx`.
- `WROTE 31 epic overviews`.
- `WROTE Day-1 Work Allocation v1.xlsx`.
- `C OK`.

- [ ] **Step 5: Run queue C at the measured budget.**

```powershell
python -I "22 Microservice Realignment/compat/run_parallel.py" --queue C
```

Expected: `RESULT {"DONE": 13}`. Rerun the same command until nothing is FAILED.

After C-DEF finishes, its defect mapping rows are written to `_work/msr/plan/defects.jsonl`, one JSON object per line with `id`, `legacy`, `story` and `note`. The C-DEF WP file says so. Before you run it, append that line to `_work/msr/wp/C-DEF.md` with this command:

```powershell
Add-Content -Encoding utf8 "_work/msr/wp/C-DEF.md" "Also write one JSON line per defect to _work/msr/plan/defects.jsonl with keys id, legacy, story, note."
```

- [ ] **Step 6: Build the epic diagrams, then run the stage checks.**

```powershell
python -I "22 Microservice Realignment/compat/build_arch_diagram.py" --epics
```

```powershell
python -I "22 Microservice Realignment/checks/run_all.py" --stage C
```

Expected: 31 `WROTE RWB-…` lines, then no FAIL. To fix a FAIL:
1. Requeue the named WPs with `requeue.py`.
2. Rerun queue C, or queue B if the finding is in a story file.
3. Rerun `assemble.py`. It keeps the existing masters, so first delete only the master versions this run created. They are listed in the edit log `_work/msr/editlog/C-assemble.md`; record them there in Step 4, by copying the WROTE lines.

---

### Task 21: Stage D — number the registers, index and hub, master diagram, full check, summary

**Files:**
- Output:
  - Gap and Assumptions Registers in folder 23
  - Queue D outputs in folder 12
  - The master and wave diagrams
  - `04 User stories/Recovery Workbench Service Story Files v1.zip`
  - Tracker v2
  - Run Summary v1

- [ ] **Step 1: D1 — number the gaps and assumptions, and rewrite every citation.**

```powershell
python -I "22 Microservice Realignment/compat/number_registers.py"
```

Expected: `D1 OK gaps=<g> (from <n>) assumptions=<a> (from <m>) files_rewritten=<k> unmapped_citations=0`.

If `unmapped_citations` is above 0, a file cites a CG or ASM id that no jsonl row has. To fix it:
1. Run `run_all.py --full` and read the C17 findings.
2. Add the missing row to that WP's jsonl.
3. Delete the two register files just written in folder 23.
4. Rerun.

- [ ] **Step 2: D2 and D3 — run queue D and build the master diagram at the same time.** Run the two commands in two terminals, or start the first in the background:

```powershell
python -I "22 Microservice Realignment/compat/run_parallel.py" --queue D
```

```powershell
python -I "22 Microservice Realignment/compat/build_arch_diagram.py" --master
```

Expected:
- `RESULT {"DONE": 6}`.
- Five `WROTE` lines: the master diagram and Waves 1–4.

Open `Recovery Workbench Microservice Architecture by Epic and Story v1.svg` and confirm two things:
- It shows the 5 bands and every epic frame.
- The legend shows the six work-type colours and the call styles.

- [ ] **Step 3: Zip the story files and write the Tracker v2.**

```powershell
Compress-Archive -Path "04 User stories/Recovery Workbench Service Story Files v1" -DestinationPath "04 User stories/Recovery Workbench Service Story Files v1.zip"
```

```powershell
python -I "22 Microservice Realignment/compat/docgen.py" tracker
```

Expected: the zip exists, then `WROTE Recovery Workbench Microservice Realignment Tracker v2.xlsx`.

- [ ] **Step 4: D4 — run the full check and fix the findings.**

```powershell
python -I "22 Microservice Realignment/checks/run_all.py" --full
```

Expected: every check PASS, or WARN for C11 and C13. C11 and C13 warn only inside preserved word-for-word copies. To fix a FAIL:
1. Requeue the WPs named in the report.
2. Rerun their queue.
3. Rerun Steps 1–4.

Never edit a baseline file to make a check pass.

- [ ] **Step 5: Write the Run Summary and finish.**

```powershell
python -I "22 Microservice Realignment/compat/docgen.py" summary
```

Expected: `WROTE Recovery Workbench Realignment Run Summary v1.md`. The run ends here. The human verification loop is a separate, later activity (U8). No commits are made (AGENTS.md rule 3).

---

## 5. Self-review (writing-plans checklist)

**1. Spec coverage.** Each user requirement mapped to the task that delivers it:

| User requirement | Delivered by |
|---|---|
| One modular epic per service, plus platform and integration epics | Task 12 (`split_plan.py`: 19 SVC, 7 PLT, 5 ITG epics); Task 20 epic overviews |
| Business-epic tags (U1) | `business_epic` field and W-MAP (Task 12); "Business epic" metadata row (§R7.1) |
| Stories in an epic run in parallel; low dependency; start the next day | Lanes ≤ 4 deep, contract-first CON stories with no dependencies, Day-1 rule (Task 12, §R5.7); C07 and C08 checks |
| Separate linked stories per team type, soft ownership, no names (U3) | Work types CON/APP/DB/INF/OPS/ITG with fixed suggested-owner phrases; C12 name check |
| Do not disturb implemented Epic 1 work (U2) | PRESERVED, MUST and BUILD_STATUS (Task 12), §R6, Change Register (Task 14), C01 baseline hashes |
| Full 19-section template (U4) | §R7, C02 and C03 |
| New versions in place, plus folders 22 and 23 (U5) | `next_version` everywhere; `office_write._guard` refuses overwrite; C01 |
| No Jira; impacts in a separate file (U6) | `opencode.json` disables the jira MCP; AGENTS.md rule 3; Jira Impact file (Task 14); C13 |
| Dates unchanged and tentative, 8 months (U7) | AGENTS.md rule 10; C15 |
| No human stops; maximum subagents (U8) | §0; Task 6 probe; Task 7 weighted budget; fanout per story WP; Stages B–D queues |
| Existing BRDs and HVE Core AI-SDLC agents for BRDs and PRDs (U9) | Tasks 3–5 (workspace copy, OpenCode agents, smoke); Task 13 `req_wps` (brd-builder, prd-builder); Task 17 context-updater; C2-RTM and C3-TC use the traceability and QA agents |
| DeepSeek v4.1 Flash in T3 Code, with a self-fixing compatibility layer | Tasks 2, 4, 5 (fallback table), 6 and 7 (retry, backoff, quota guard); AGENTS.md rule 13 |
| Gap folder with versions, plus a separate Assumptions register | Task 15; folder 23; seed rows; D1 numbering |
| Big technical Excalidraw diagram by epic and story (U10) | Task 18; Task 20 Step 6; Task 21 Step 2 |
| Save the plan at ROOT; the writing-plans skill must not reduce parallelism | Plan header and §0.1; Task 1 Step 7 |

**2. Placeholder scan.** Each `<n>` in an "Expected" line is a count the script prints; it is not a value to fill in. No step says TBD, "similar to", or "add error handling".

**3. Type consistency.** These names are defined once and used the same way in every later task:
- Slice keys: `id`, `scope`, `wt`, `epic`, `lane`, `ready`, `owner`, `H`, `C`, `I`, `X`, `acs`, `file`, `preserved`, `delta`, `wave`, `business_epic`, `release`, `legacy`.
- Queue item keys: `wp`, `agent`, `file`, `fanout`, `expect`.
- Fragment keys (from STORY_RULES in Task 13), read by C06–C10, `assemble.py` and `build_arch_diagram.py`.
- `OWNER` keys: TechX, ACE, INFRA, DEVOPS, QA.

**Known limits, accepted:**
- The PRDs (Stage B) read the v4 BRDs, not the new BRD versions written in the same stage. BRD business content is unchanged by the realignment, so the PRDs stay valid.
- The live concurrency probe could not run while planning. Task 6 measures it at run time, and the history (10 subagents per session, 19 sessions machine-wide, 0 rate-limit lines) is the fallback.

---

## 6. How to start the run

In T3 Code, open an OpenCode session at ROOT with model `opencode-go/deepseek-v4.1-flash` (variant max) and send:

> Execute `2026-11-22-recovery-microservice-realignment-implementation-plan.md` from Task 1 to Task 21 in order. Follow AGENTS.md. Do not stop to ask questions. Tick each checkbox in the plan file as you finish it.

---

## Appendix R — Rules reference

<!-- R-TEMPLATE-BEGIN -->
## R1. User decisions (fixed for this run)

| ID | Decision |
|---|---|
| U1 | One epic per service (19), plus 7 platform and 5 integration epics. Every story also carries its business epic (EP01–EP08) as a tag. |
| U2 | Work already built or in build in Epic 1 is not changed unless absolutely needed. It is kept word for word, and the microservice change goes into separate delta stories. |
| U3 | Separate linked stories per team type. The owner is a suggestion only ("any team may pick up this story"). No names of people anywhere. |
| U4 | Every story uses the full 19-section template in §R7. |
| U5 | New versions sit next to the old ones in the same folders. Run material goes to folder 22, and gaps and assumptions to folder 23. |
| U6 | No issue-tracker access or updates. Tracker impacts go to one separate file only. |
| U7 | Dates are tentative and unchanged; the programme finishes within 8 months. A date is never raised as a gap. |
| U8 | No human verification stops in this run; maximum parallel agents. The verification loop comes later. |
| U9 | The BRDs and PRDs are produced with the existing BRDs and the AI-SDLC (HVE Core) agents. |
| U10 | A large technical Excalidraw diagram, by epic and story, for developers and architects. |
<!-- R-TEMPLATE-END -->

<!-- R-JIRA-BEGIN -->
## R2. Jira impact (for the separate follow-up file only)

This run makes no Jira change and reads nothing from Jira. A person with Jira access applies the follow-ups below later. The epic and story IDs are the new IDs in the Service Story Catalog v1.

| Legacy disposition | Follow-up in Jira |
|---|---|
| Retired (D-RCV-53) | Close the issue as won't do, with resolution note "Retired by D-RCV-53". Do not delete it. |
| Already retired | No change. |
| Preserved + delta | Keep the issue, its status, sprint and history. Create the delta and contract issues and link them with "relates to". |
| Must change (RWB-E1-001) | Keep the issue and its status. Add a comment with the Change Register row. Create the linked DB split issues. |
| Moved (no impact) | Keep the issue. Change its epic link to the new service epic. Add the business-epic label. |
| Split (rework) | Keep the issue as the main APP story in the service epic. Create the linked CON, DB, INF, OPS and ITG issues. |
| New | Create the issue in its epic, with the suggested-owner text as a label, not as an assignee. |

Create the 31 epics first: 7 PLT, 19 SVC and 5 ITG. Then create stories in this order: CON, then DB, INF and OPS, then APP, then ITG. Each story's dependency links come from the "Dependencies" sheet of the catalogue.
<!-- R-JIRA-END -->

<!-- R-TEMPLATE-BEGIN -->
## R3. Source precedence (R-PREC) and default rulings

When two sources disagree, the higher one in this list wins. The loser is recorded as a gap row (type Conflict) and an assumption row.

1. Arch v5 catalogue slides (services, resources, call types: slides 13–20 and 41–44).
2. Recovery Temporal and Drools Detailed Design v1.
3. Arch v5 narrative slides.
4. Decision Log (latest version).
5. Architecture Decision Records (latest version).
6. Technical Specifications by Module (latest version).
7. Functional Specifications by Module (latest version).
8. Physical Schema and Logical Data Model (latest version).
9. The story masters.

**Default rulings.** Each ruling is also an assumption in the Assumptions Register.

| Item | Owner |
|---|---|
| Parameters and reference data (E1-042, E1-043) | P3 rwb-case |
| Case list API | P3 rwb-case |
| Rule package registry | P7 rwb-decision |
| Interaction ledger | P1 rwb-source-data |
| Feature flags | Platform library |

## R4. Services and naming

The service table has 19 rows; the source is Arch v5. Each service has:
- schema `rwb_<short with _>`
- login per service
- REST base `/api/recovery/<short>/v1`
- topic `rwb.<short>.events.v1`, with retry and `.dlt` topics
- event names `rwb.<short>.<Event>.v1`
- Temporal task queue `rwb-<short>`
- Java package `th.co.scb.ace.workbench.recovery.<short without hyphen>`
- epic `RWB-SVC-<code>`

**Platform (wave 0) and integration:**

| Code | Service | Wave | Code | Service | Wave |
|---|---|---|---|---|---|
| P1 | rwb-source-data | 1 | S1 | rwb-valuation | 3 |
| P2 | rwb-integration | 1 | S2 | rwb-treatment | 2 |
| P3 | rwb-case | 1 | S3 | rwb-guarantee | 3 |
| P4 | rwb-access | 1 | S4 | rwb-litigation | 3 |
| P5 | rwb-document | 1 | S5 | rwb-asset | 2 |
| P6 | rwb-comms | 1 | S6 | rwb-debtsale | 3 |
| P7 | rwb-decision | 1 | S7 | rwb-writeoff | 4 |
| P8 | rwb-payment | 2 | S8 | rwb-deviation | 2 |
| P9 | rwb-reporting | 1 | S9 | rwb-partner | 4 |
| P10 | rwb-agent | 1 | | | |

Shared topic: `rwb.decision-record.v1`. Temporal namespace: `rwb-recovery`. Edge: gateway-bff (Redis session store) and the partner gateway in the DMZ.

## R5. Target structure

### R5.1 Epics

- **Platform:**
  - RWB-PLT-TPL: service template and repositories
  - RWB-PLT-LIB: shared libraries
  - RWB-PLT-WF: Temporal workflow platform
  - RWB-PLT-DB: ACE DB schemas and logins
  - RWB-PLT-EVT: Kafka event platform
  - RWB-PLT-EDGE: edge and gateway
  - RWB-PLT-OBS: observability
- **Service:** RWB-SVC-P1 … RWB-SVC-S9.
- **Integration:**
  - RWB-ITG-W1 … RWB-ITG-W4: one per wave
  - RWB-ITG-NFR: non-functional

### R5.2 Story IDs

Pattern: `RWB-<scope>-<legacy compact>-<work type>[-n]`.
- Scope: P1–P10, S1–S9, PLT or ITG.
- Legacy compact: E1018, TE001, AD003, DM002, ACE001, NF06, N001 (new), or W1J01 (new integration).
- `-2` is the delta copy of a preserved story that keeps its base ID.

Example: `RWB-P3-E1018-APP`.

### R5.3 Work types and suggested owners

| Work type | Name | Suggested owner (fixed phrase) |
|---|---|---|
| CON | Contract | TechX (suggested; any team may pick up this story) |
| APP | App development | TechX (suggested; any team may pick up this story) |
| DB | ACE DB | ACE team (suggested; any team may pick up this story) |
| INF | Infrastructure | SCB IT infrastructure (suggested; any team may pick up this story) |
| OPS | DevOps | DevOps team (suggested; any team may pick up this story) |
| ITG | Integration | TechX (suggested; any team may pick up this story). Harness and NFR stories: QA team (suggested; any team may pick up this story) |

### R5.4 Dependency classes

| Class | Meaning | Blocks the build? |
|---|---|---|
| H | Same service, or a platform CON story | Only H on a non-CON story (same lane) |
| C | Another service's CON story. Build against the published contract and its fake. | No |
| I | The real cross-service behaviour. Allowed only on ITG stories. | ITG only |
| X | External or team-type work (DB, INF or OPS story of the same legacy key, outside systems) | No; tracked |

### R5.5 Decoupling patterns (DP table)

| DP | Legacy marker | Microservice pattern | Dependency added |
|---|---|---|---|
| DP-01 | `recovery.<table>` or "recovery schema" | Owner's schema `rwb_<name>`; never read another service's tables | none |
| DP-02 | `recovery_svc` login | One login per service | none |
| DP-03 | DecisionLogWriter, decision log | Local decision-record library and topic `rwb.decision-record.v1` | H RWB-PLT-E1027-CON |
| DP-04 | RuleEvaluator, Drools | Embedded Drools kit; rule packages from rwb-decision | H RWB-PLT-E1072-CON; C RWB-P7-E1073-CON |
| DP-05 | AceSourceQuery, `v_ace_*`, account_ext | Read through rwb-source-data's contract or the service's own ACE views | none |
| DP-06 | Parameters, casewf.config | Parameters contract of rwb-case and the client library | H RWB-PLT-E1042-CON; C RWB-P3-E1042-CON |
| DP-07 | Reference data, LOV | Reference-data contract of rwb-case | H RWB-PLT-E1043-CON; C RWB-P3-E1043-CON |
| DP-08 | RecoveryAccessGuard | Authorise contract of rwb-access and the guard library | H RWB-PLT-E1037-CON; C RWB-P4-E1037-CON |
| DP-09 | Application event, EV-nn, outbox | Outbox and inbox library; Kafka topic of the owner; CloudEvents | H RWB-PLT-TE006-CON |
| DP-10 | Quartz, JOB-nn | Temporal Schedule or event-started workflow through the workflow kit | H RWB-PLT-E1071-CON |
| DP-11 | In-process call, published interface | REST contract with mock; one hop; 2 s timeout | none (C from the legacy dependency) |
| DP-12 | One workflow per case | CaseWorkflow parent with a child workflow per stage | none |
| DP-13 | `/api/recovery/v1` | `/api/recovery/<short>/v1` | none |
| DP-14 | `rwb.p<n>.` or `rwb.casewf.` topic names | `rwb.<short>.events.v1`; naming library | H RWB-PLT-E1047-CON |
| DP-15 | V0001 baseline, migration | Per-service Flyway sequence in the service's own schema | H RWB-PLT-E1044-CON |
| DP-16 | `recovery.integration.adapter` | rwb-integration contract | C RWB-P2-E1007-CON |
| DP-17 | Data lake, INT-19, INT-20 | Removed (no data lake); reporting from events into rwb-reporting | none; gap if the story needs lake data |
| DP-18 | Interaction ledger | Ledger owned by rwb-source-data (default ruling) | none |
| DP-19 | Screen, ace-web | gateway-bff composite route | H RWB-PLT-N001-CON |
| DP-20 | Agent client | rwb-agent contract | C RWB-P10-TE013-CON |

### R5.6 Wave map (W-MAP)

| Business epic | Wave |
|---|---|
| EP01 | 1 |
| EP02, EP03 | 2 |
| EP04, EP05 | 3 |
| EP06, EP07, EP08 | 4 |
| Platform and NF | 0 |

A story whose W-MAP wave is earlier than its service's Arch v5 wave keeps the W-MAP wave. One conflict gap is raised per service and business epic.

### R5.7 Lanes and Day-1 rules

1. A CON story has no build dependency. It is always "Day 1" and sits in contract group `CG-W<wave>`.
2. An APP story builds against CON stories and their fakes. C dependencies never block.
3. H dependencies point only to the same service, or to a platform CON story.
4. I dependencies sit only on ITG stories.
5. A lane is a connected group of non-CON stories linked by H. Its depth is at most 4. A deeper chain is cut: the later story builds against the earlier story's CON (created if missing), and an assumption is recorded.
6. Every team type has Day-1 work. The new platform stories N001–N012 and the integration harness W1J01 make sure of this.
7. Every service has at least one CON story. A service with none gets a "service contract baseline" story (N013 onwards).
8. Ready to start = "Day 1" if the story has only CON H dependencies; otherwise "After <the in-lane story IDs it waits for>".

## R6. Epic 1 preservation

| Group | Stories | Rule |
|---|---|---|
| Built or in build, preserved | RWB-TE-001, TE-002, TE-003, E1-042, E1-043, E1-044 | The as-built story keeps its base ID with `preserved=true`. Legacy sections 1–11, 14–16, 18 and 19 are copied word for word. Sections 12 and 13 sit under "As built (monolith)". The microservice change is a separate delta story (`-2` copy, or CON/OPS stories). No change to built code until a delta story is picked up. |
| Must change | RWB-E1-001 | In build: the single recovery schema (92 tables, 14 data products, dictionary). The built migration is kept. The split into rwb_* schemas is new work (RWB-PLT-NF06-DB and the per-service DB stories). It is recorded in the Change Register. |
| Retired | RWB-E1-014 (decision log copy to the data lake: no data lake in Arch v5); RWB-TE-007 (Quartz scheduler: replaced by Temporal Schedules in RWB-PLT-E1071) | No new story. Dependencies on E1-014 are dropped. Dependencies on TE-007 point to RWB-PLT-E1071-CON. |
| Already cancelled | E1-003, 004, 005, 006, 009, 010, 012, 029, 048, 051; TE-005 | No new story. |
| No impact | E1-024, 025, 026, 033, 034, 038, 040, 041, 045, 053, 060, 061, 068; TE-010, TE-012 | Moved to their epic with content unchanged. |

## R7. Story template

### R7.1 Metadata table

The story's first line is `# <Story key> <Title>`. Next comes `| Item | Value |` with these rows, in this order, and none may be removed:

1. Story key
2. Work type
3. Suggested owner
4. Service
5. Service epic
6. Wave
7. Business epic
8. Release
9. Legacy key
10. Legacy disposition
11. Build status
12. Patterns applied
13. Parallel lane
14. Ready to start
15. Depends on (build)
16. Contract dependencies
17. Integration dependencies
18. External dependencies
19. PRD reference
20. Status

### R7.2 The 19 sections

Use `### n. Name`, in this order:

| # | Section | # | Section |
|---|---|---|---|
| 1 | Story | 11 | Data |
| 2 | Business rationale | 12 | Contract |
| 3 | Preconditions | 13 | Solution plan |
| 4 | Flow | 14 | Validation and messages |
| 5 | Exception paths | 15 | Screens and states |
| 6 | INVEST check | 16 | Test cases |
| 7 | Acceptance criteria | 17 | Guardrails |
| 8 | Business rules | 18 | Traceability |
| 9 | State transitions | 19 | Out of scope |
| 10 | Authority | | |

**Section rules:**
- **s7 Acceptance criteria.** Each `Scenario: ACn` line ends with an origin tag, either "(legacy RWB-…-nnn ACn)" or "(new, D-RCV-53)".
- **s12 Contract.** Tables 12.1–12.9, written "None" where empty:
  - 12.1 REST operations provided
  - 12.2 REST operations consumed
  - 12.3 Events published
  - 12.4 Events consumed
  - 12.5 Workflows and activities
  - 12.6 Schedules
  - 12.7 Tables owned
  - 12.8 Contract fakes
  - 12.9 Call-type summary (REST, Kafka, Temporal, File)
- **s16 Test cases.** Table columns: TC ID, Covers, Level (Unit, Component, Contract, Integration, End to end, NFR), Data. ITG copies of a TC end in `-ITG`.
- **s17 Guardrails.** No business values in code, no PII in events, workflow inputs or logs, ACE data only through the owner's contract or `v_ace_*` views.

### R7.3 Fill order for thin stories (Epics 3 to 8)

Take each value from the first source in this list that has it:
1. The legacy story
2. The FSD module file
3. The TSD module file
4. The BRD (Program, then the epic BRD)
5. Business Rules and Routing Logic
6. The Arch v5 extract

If no source has the value, write the placeholder in §R9 and add a gap row and an assumption row. Never invent business values.

## R8. Outputs

### R8.1 Header

Every new document starts with these two lines:

```
SCB Collections and Recovery. Henka Group, 22 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd
```

Every new document also has a change-log row naming D-RCV-53 and the tool line "T3 Code / OpenCode / DeepSeek v4.1 Flash".

### R8.2 Versioning

- The next version is the highest `v<n>` of the family plus 1, in the same folder.
- An existing file is never edited.
- A folder family is copied to the next-version folder, and only the files that change get a new version inside it.

### R8.3 Folders 22 and 23

**Folder 22** holds the run material:
- Text Extracts v1
- Ownership Map v1
- Template and Rules v1
- Change Register v1
- Tracker v1 and v2
- Jira Impact and Follow-up v1
- the architecture diagrams
- Run Summary v1
- `compat/`, `checks/` and `aisdlc/`

**Folder 23** holds the Gap Register and Assumptions Register (xlsx and md).

### R8.4 Architecture outputs

**ADRs.** Add ADR-013 to ADR-023, or the IDs allocated in `ids.json`. Each one supersedes or amends the decision named after the dash:

| ADR | Decision |
|---|---|
| 013 | 19 services inside ACE — supersedes the single-service decision ADR-002 |
| 014 | Schema and login per service in ACE PostgreSQL |
| 015 | Kafka with outbox, inbox and CloudEvents |
| 016 | Reusable Temporal layer; Schedules replace Quartz |
| 017 | Embedded Drools per service; rule registry in rwb-decision — amends D-RCV-36 T1 and T2 |
| 018 | No data lake; rwb-reporting read model from events |
| 019 | Edge: gateway-bff and partner gateway |
| 020 | Contract-first REST, one hop, 2 s timeout |
| 021 | Per-service Flyway and migration ownership |
| 022 | Local decision record plus central ledger |
| 023 | Observability per service |

**Decision Log.** Add D-RCV-53 (adopt Arch v5 and realign the documents and stories), plus:

| Row | Decision |
|---|---|
| DL44 | Adopt Arch v5 |
| DL45 | Service epics plus business-epic tags |
| DL46 | Soft ownership by team type |
| DL47 | Epic 1 preservation rule |
| DL48 | Dates unchanged and tentative |
| DL49 | Gap and assumption registers |

**Other architecture outputs:**
- Service Catalog v1
- Service Template Specification v1
- API Specification split into 19 files plus gateway-bff and an index
- Event and Messaging next version, plus the Kafka Topic and Event Catalog v1
- Batch and Scheduling next version, plus the Temporal Workflow and Activity Catalog v1
- Physical Schema folder with 19 `rwb_<name>.sql` files, plus `recovery_views.sql` and a README
- LDM and ERD next versions
- Service Contract Catalog v1

### R8.5 Requirements outputs

- **BRDs (BRD Builder):**
  - Program, Epic 1 and Epic 2: next versions, with BR IDs stable plus a "Delivery model" section
  - Epics 3 to 8: new v1
- **PRDs (PRD Builder):** 20 files: one per service plus Platform, in `03 Requirements and specifications/PRD/`.

### R8.6 Document families

The 49 families, and what changes in each, are listed in `make_wps.py` `DOCS` (Task 13).

### R8.7 Story outputs

- **Story files:** `04 User stories/Recovery Workbench Service Story Files v1/<epic> <epic name>/RWB <scope> <legacy> <WT> <title><suffix> v1.md`
- **New versions of the 7 masters**
- **Service Story Catalog v1:** one per story set, with:
  - an epic overview per epic folder
  - the Day-1 Work Allocation v1
  - the Service Epics v1 file
- **Next versions of these files:**
  - RTM
  - Test Cases
  - Regression Suite
  - Build Sequence
  - Story Build Order
  - Dependency Map
  - Story Defects
  - Worked Example
  - AC Glossary
  - How To Read The Acceptance Criteria
  - Build Notes for E1, E2 and the Technical Enablers

### R8.8 Diagram styles

**Work types:**

| Type | Colour |
|---|---|
| CON | blue `#1971c2` |
| APP | green `#2f9e44` |
| DB | brown `#8d5524` |
| INF | grey `#868e96` |
| OPS | purple `#7048e8` |
| ITG | red `#e03131` |

**Calls:**

| Call | Style |
|---|---|
| Build dependency (H) | thin black |
| REST | solid blue |
| Kafka | dashed orange |
| Temporal | solid purple |
| File | dotted grey |
| Integration dependency (I) | dashed red |

**Layout:** wave bands (0 platform, 1–4, then integration) → epic frames → lane columns → story boxes.

## R9. Gaps and assumptions

**Placeholder.** Where a value is missing, write: `Not specified in the source documents (CG-<WP>-<n>; ASM-<WP>-<n>)`.

**Candidate rows.** Each WP writes one JSON object per line to `_work/msr/gaps/<WP>.jsonl` and `_work/msr/assumptions/<WP>.jsonl`.
- **Gap row keys:** id, title, source, section, description, evidence, type, area, severity, needed_by_wave, legacy_ref, owner_role, asm, proposed, wp.
- **Assumption row keys:** id, text, why, read, gap, applied_in, confidence, confirm, impact, wp.

**Numbering.** Only step D1 numbers the rows, as GAP-nnnn and ASM-nnnn, and rewrites every citation.

**Gap types:**
- Missing
- Conflict
- Ambiguous
- Outdated
- ID collision

**Severity:**
- P1: blocks a wave start.
- P2: blocks a story's Done.
- P3: documentation only.

**Confidence:** High, Medium or Low.
<!-- R-TEMPLATE-END -->

## R10. Checks

| Check | What it proves |
|---|---|
| C01 | No baseline file changed or disappeared (sha256 against `baseline.json`) |
| C02 | Valid story ID on the title line; all 20 metadata rows in order |
| C03 | The 19 section headings in order |
| C04 | Every planned story has a file |
| C05 | Every AC line has an origin tag |
| C06 | H dependencies are same-service or contract; I dependencies only on ITG stories |
| C07 | No cycle; lane depth ≤ 4 |
| C08 | Day-1 work for every team type |
| C09 | Every live legacy story has new stories; preserved stories keep "As built (monolith)" |
| C10 | Every legacy AC is owned by a new story |
| C11 | Every legacy TC appears in a new story (WARN) |
| C12 | No person names (deny-list in memory only) and no email addresses |
| C13 | No issue-tracker references outside the Jira impact file (WARN inside preserved copies) |
| C14 | Document header lines present |
| C15 | Release dates unchanged and marked tentative |
| C16 | Service names in topics, bases and queues are real; no old API base outside the as-built section |
| C17 | Gap and assumption rows are complete; every citation has a row |
| C18 | The WP wrote only its "Write only" files; legacy masters unchanged |
| C19 | Every planned output exists and carries the D-RCV-53 change-log row |
| C20 | Tool line in every edit log; no wrong tool attribution |

## R11. Risks

| ID | Risk | Response in this plan |
|---|---|---|
| R1 | OpenCode does not load the generated agents | Smoke test with layout fallback and a plain-worker fallback (Task 5) |
| R2 | Provider quota or rate limit during fan-out | Quota guard, backoff, budget lowered by 2 and raised again; rerun skips DONE (Task 7) |
| R3 | Agent writes outside its WP | AGENTS.md rules 1–2, C18, C01 baseline |
| R4 | Agent invents business values | Placeholder rule, gap and assumption rows, origin tags (C05) |
| R5 | Built Epic 1 work disturbed | Preserved copies, delta stories, Change Register, C01 |
| R6 | Ownership conflicts between sources | R-PREC, default rulings, Conflict gaps |
| R7 | Long dependency chains block teams | Contract-first CON stories, lane depth cut ≤ 4, Day-1 rule (C07, C08) |
| R8 | Person names leak from source documents | C12 deny-list in memory only; roles only |
| R9 | Office formats damaged by text edits | `office_write.py` copies and appends; never edits in place |
