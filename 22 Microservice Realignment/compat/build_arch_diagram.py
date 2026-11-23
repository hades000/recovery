"""Excalidraw v2 diagrams by epic and story, plus an SVG render of the same elements. Deterministic layout."""
import argparse, hashlib, html, json, sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
from common import ROOT, R22, WORK, SERVICES, read_json, write_json, decision

DEC = decision()

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
            save(build([x for x in slices if x["id"] in ids], frags, f"{epic} - stories, lanes and contracts ({DEC})", own), d / epic)
    else:
        save(build(slices, frags, f"Recovery Workbench microservice architecture by epic and story v1 ({DEC})", own),
             R22 / "Recovery Workbench Microservice Architecture by Epic and Story v1")
        for w in (1, 2, 3, 4):
            ss = [x for x in slices if x["wave"] == w or (x["wave"] == 0 and w == 1)]
            save(build(ss, frags, f"Recovery Workbench Wave {w} architecture v1 ({DEC})", own), R22 / f"Recovery Workbench Wave {w} Architecture v1")
    write_json(WORK / "plan" / "diagram_written.json", {"done": True})
