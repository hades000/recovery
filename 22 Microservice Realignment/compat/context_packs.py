"""Build compact per-service context packs for the remaining realignment work packages.

Each pack replaces the two large extracts (Architecture v5, Temporal/Drools) and the full
ownership JSON in the read list of a story WP. It contains only what that service needs:
the service row, naming rules, the ownership rows it owns, the matching architecture
slides, and the FSD/TSD file paths.
"""
import json, re, sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
from common import ROOT, R22, WORK, SERVICES, svc, read_json

ARCH = R22 / "Recovery Workbench Architecture v5 Text Extract v1.md"
TD = R22 / "Recovery Workbench Temporal and Drools Design Text Extract v1.md"
EX = WORK / "extract"
OUT = WORK / "context"
OWN = read_json(WORK / "plan" / "ownership.json", {}) or {}

PLATFORM_EPICS = ["RWB-PLT-TPL", "RWB-PLT-LIB", "RWB-PLT-WF", "RWB-PLT-DB", "RWB-PLT-EVT", "RWB-PLT-EDGE", "RWB-PLT-OBS"]
INTEGRATION_EPICS = ["RWB-ITG-W1", "RWB-ITG-W2", "RWB-ITG-W3", "RWB-ITG-W4", "RWB-ITG-NFR"]
SHARED = """## Naming and shared platform rules
- 19 services inside ACE. One PostgreSQL schema and one login per service.
- Schema `rwb_<short with _>`; REST base `/api/recovery/<short>/v1`; topic `rwb.<short>.events.v1`;
  event name `rwb.<short>.<Event>.v1`; Temporal task queue `rwb-<short>`;
  Java package `th.co.scb.ace.workbench.recovery.<short without hyphen>`.
- Shared topic `rwb.decision-record.v1`; Temporal namespace `rwb-recovery`.
- Kafka with outbox and inbox, CloudEvents envelope. Retry and `.dlt` topics per service.
- Temporal Schedules replace Quartz. Embedded Drools per service; rule packages come from rwb-decision.
- Contract-first REST: one hop, 2 s timeout. No service reads another service's tables.
- No data lake. rwb-reporting builds its read model from events.
- No PII in events, workflow inputs or logs. ACE data only through the owner's contract or `v_ace_*` views.
## Decoupling patterns (DP table, short)
DP-01 own schema only | DP-02 one login per service | DP-03 local decision record + rwb.decision-record.v1 |
DP-04 embedded Drools + rule packages from rwb-decision | DP-05 ACE data through rwb-source-data or v_ace_* |
DP-06 parameters contract of rwb-case | DP-07 reference data contract of rwb-case |
DP-08 authorise contract of rwb-access | DP-09 outbox/inbox + owner topic |
DP-10 Temporal Schedule or event-started workflow | DP-11 REST contract with mock |
DP-12 CaseWorkflow parent with child per stage | DP-13 per-service API base |
DP-14 per-service topic names | DP-15 per-service Flyway |
DP-16 rwb-integration contract | DP-17 no data lake |
DP-18 interaction ledger owned by rwb-source-data | DP-19 gateway-bff composite route |
DP-20 rwb-agent contract.
"""

def slides(path):
    if not path.exists():
        return []
    text = path.read_text(encoding="utf-8", errors="replace")
    parts = re.split(r"(?m)^## Slide ", text)
    return ["## Slide " + p for p in parts[1:]]

def pick_slides(path, patterns, limit=5, cap=2600):
    out, seen = [], set()
    for s in slides(path):
        low = s.lower()
        if any(re.search(p, s, re.I) for p in patterns):
            key = s[:90]
            if key in seen:
                continue
            seen.add(key)
            out.append(s[:cap].rstrip() + ("…" if len(s) > cap else ""))
            if len(out) >= limit:
                return out
    return out

def rows(owner, key, cap=None):
    items = [(k, v) for k, v in (OWN.get(key) or {}).items() if v.get("owner") == owner]
    items.sort(key=lambda kv: kv[0])
    return items[:cap] if cap else items

def bullet_rows(items, limit=None, detail=False):
    out = []
    for k, v in (items[:limit] if limit else items):
        if detail and v.get("basis"):
            out.append(f"- {k} — {v.get('basis')}")
        else:
            out.append(f"- {k}")
    if limit and len(items) > limit:
        out.append(f"- … and {len(items) - limit} more")
    return out

def file_lines(code):
    out = []
    for pat in (f"Recovery Workbench FSD {code} *.md", f"Recovery Workbench TSD {code} *.md"):
        for p in sorted(EX.glob(pat)):
            out.append(f"- {p.relative_to(ROOT).as_posix()}")
    return out

def service_pack(s):
    code = s["code"]
    out = [f"# Context pack — {code} {s['service']} ({s['name']})",
           "",
           "Read this pack instead of the full Architecture v5 and Temporal/Drools extracts and the full ownership JSON.",
           "",
           "## Service",
           f"- Code: {code}",
           f"- Service: {s['service']}",
           f"- Display name: {s['name']}",
           f"- Schema: {s['schema']}",
           f"- REST base: {s['base']}",
           f"- Topic: {s['topic']}",
           f"- Queue: {s['queue']}",
           f"- Epic: {s['epic']}",
           f"- Wave: {s['wave']}",
           f"- Java package: {s['package']}",
           "",
           SHARED,
           f"## Ownership rows owned by {code}"]
    for label, key in (("Tables", "tables"), ("REST operations provided", "api"),
                       ("Events", "events"), ("Jobs", "jobs"), ("Workflows", "workflows")):
        items = rows(code, key)
        out.append(f"### {label} ({len(items)})")
        out += bullet_rows(items, limit=(60 if key == "api" else None)) if items else ["- None"]
        out.append("")
    arch = pick_slides(ARCH, [re.escape(s["service"]), rf"\b{re.escape(code)}\b"], limit=5)
    if arch:
        out += ["## Architecture v5 slides that name this service", ""] + arch + [""]
    td = pick_slides(TD, [re.escape(s["service"]), rf"\b{re.escape(code)}\b"], limit=3)
    if td:
        out += ["## Temporal and Drools slides that name this service", ""] + td + [""]
    fl = file_lines(code)
    if fl:
        out += ["## Module source files (read the ones named in your WP)", ""] + fl + [""]
    return out

def plt_pack():
    out = ["# Context pack — PLT Platform",
           "",
           "Read this pack instead of the full Architecture v5 and Temporal/Drools extracts and the full ownership JSON.",
           "",
           "## Platform scope",
           "- 7 platform epics, wave 0: " + ", ".join(PLATFORM_EPICS),
           "- Platform owns shared libraries, the Temporal layer, Kafka platform, ACE DB schemas and logins, edge/gateway, observability and the service template.",
           "",
           SHARED,
           "## Ownership rows owned by PLT"]
    for label, key in (("Tables", "tables"), ("REST operations provided", "api"),
                       ("Events", "events"), ("Jobs", "jobs"), ("Workflows", "workflows")):
        items = rows("PLT", key)
        out.append(f"### {label} ({len(items)})")
        out += bullet_rows(items) if items else ["- None"]
        out.append("")
    arch = pick_slides(ARCH, [r"platform", r"template", r"Kafka", r"gateway", r"observ", r"Temporal"], limit=6)
    if arch:
        out += ["## Architecture v5 platform slides", ""] + arch + [""]
    td = pick_slides(TD, [r"platform", r"namespace", r"schedule", r"workflow kit"], limit=4)
    if td:
        out += ["## Temporal and Drools platform slides", ""] + td + [""]
    return out

def itg_pack():
    out = ["# Context pack — ITG Integration",
           "",
           "Read this pack instead of the full Architecture v5 and Temporal/Drools extracts and the full ownership JSON.",
           "",
           "## Integration scope",
           "- Integration epics: " + ", ".join(INTEGRATION_EPICS),
           "- One journey per wave plus the NFR integration epic.",
           "",
           SHARED,
           "## Services (19)",
           "| Code | Service | Schema | REST base | Topic | Wave |",
           "|---|---|---|---|---|---|"]
    for s in SERVICES:
        out.append(f"| {s['code']} | {s['service']} | {s['schema']} | {s['base']} | {s['topic']} | {s['wave']} |")
    out += ["", "## REST operations by owner"]
    for code in [s["code"] for s in SERVICES] + ["PLT"]:
        items = rows(code, "api")
        if items:
            out.append(f"### {code}")
            out += [f"- {k}" for k, _ in items]
    out += ["", "## Events by owner"]
    for code in [s["code"] for s in SERVICES] + ["PLT"]:
        items = rows(code, "events")
        if items:
            out.append(f"- {code}: " + ", ".join(k for k, _ in items))
    arch = pick_slides(ARCH, [r"\bwave\b", r"integration", r"gateway", r"journey"], limit=6)
    if arch:
        out += ["", "## Architecture v5 integration slides", ""] + arch
    return out

def main():
    OUT.mkdir(parents=True, exist_ok=True)
    sizes = {}
    for s in SERVICES:
        lines = service_pack(s)
        p = OUT / f"{s['code']}.md"
        p.write_text("\n".join(lines).rstrip() + "\n", encoding="utf-8")
        sizes[s["code"]] = p.stat().st_size
    for name, lines in (("PLT", plt_pack()), ("ITG", itg_pack())):
        p = OUT / f"{name}.md"
        p.write_text("\n".join(lines).rstrip() + "\n", encoding="utf-8")
        sizes[name] = p.stat().st_size
    print("CONTEXT OK", len(sizes), "packs", "min", min(sizes.values()), "max", max(sizes.values()))
    print(json.dumps(sizes, sort_keys=True))

if __name__ == "__main__":
    main()
