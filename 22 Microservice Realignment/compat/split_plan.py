"""Deterministic split of every legacy story into service/platform/integration slices (Appendix R §R5-R6)."""
import re, string, sys
from pathlib import Path
import networkx as nx
sys.path.insert(0, str(Path(__file__).resolve().parent))
from common import (ROOT, STORIES, WORK, SERVICES, OWNER, WT_OWNER, WT_SUFFIX, svc, story_id, leg_compact,
                    read_json, write_json, reset_cands, add_gap, add_asm, decision)

DEC = decision()
RETIRED = f"Retired ({DEC})"
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
            legacy[k] = {"disposition": RETIRED, "slices": []}; continue
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
        if lg.get("disposition") in (RETIRED, "Already retired"): continue
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
