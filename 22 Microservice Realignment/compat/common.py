"""Shared paths, constants and helpers for the D-RCV-53 realignment run. Run all scripts as python -I."""
import datetime, hashlib, json, os, re, shutil, threading, time
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
    for attempt in range(12):
        try:
            os.replace(tmp, path); return
        except PermissionError:
            time.sleep(0.25)
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

def decision():
    """The decision ID allocated by id_scan.py (A5). D-RCV-53 when no allocation exists (tests)."""
    ids = read_json(WORK / "plan" / "ids.json", {}) or {}
    return ids.get("realignment_decision") or DECISION

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
