"""Source loading for the deterministic story checks (sandbox prototype, D-RCV-60).

Reads the converted markdown copies made by the project's own converter
(22 Microservice Realignment/compat/convert_sources.py) and the plain-text
sources (yaml, md, csv). Never writes inside ROOT.
"""
import csv, os, re, subprocess, sys
from pathlib import Path

# Converted source files: logical name -> path relative to ROOT
SOURCES = {
    "refdata": "06 Data/Recovery Workbench Reference Data and Lists of Values v5.xlsx",
    "casemodel": "02 Business architecture and process/Recovery Workbench Case and Workflow Model v6.xlsx",
    "ldm": "06 Data/Recovery Workbench Logical Data Model and Data Dictionary v9.xlsx",
    "ldm_prev": "06 Data/Recovery Workbench Logical Data Model and Data Dictionary v8.xlsx",
    "dclass": "06 Data/Recovery Workbench Data Classification and Personal Data Inventory v5.xlsx",
    "declog": "01 Decisions and governance/Recovery Workbench Decision Log v11.xlsx",
    "kafka": "05 Technical architecture/Recovery Workbench Kafka Topic and Event Catalog v1.xlsx",
    "temporal": "05 Technical architecture/Recovery Workbench Temporal Workflow and Activity Catalog v1.xlsx",
    "msgstd": "07 Screens and experience/Recovery Workbench Error and Message Standard v4.docx",
    "tc": "09 Testing and quality/Recovery Workbench Test Cases v8.xlsx",
    "rtm": "09 Testing and quality/Recovery Workbench Requirements Traceability Matrix v7.xlsx",
    "rules": "02 Business architecture and process/Recovery Workbench Business Rules and Routing Logic v4.xlsx",
}
TEXT = {
    "docindex": "12 Project communication/Recovery Workbench Document Index v14.md",
    "gapreg": "23 Document Gaps/Recovery Workbench Gap Register v1.md",
    "asmreg": "23 Document Gaps/Recovery Workbench Assumptions Register v1.md",
    "screens": "07 Screens and experience/Recovery Workbench Screen Specifications v1.md",
    "params": "parameter-catalog.csv",
    "apidir": "05 Technical architecture/Recovery Workbench API Specification v5",
    "stories": "04 User stories/Recovery Workbench Service Story Files v1",
    "prddir": "03 Requirements and specifications/PRD",
}

PIPE = re.compile(r"(?<!\\)\|")


def split_row(line):
    line = line.strip()
    if not line.startswith("|"):
        return None
    parts = PIPE.split(line)[1:-1] if line.endswith("|") else PIPE.split(line)[1:]
    return [p.strip().replace("\\|", "|") for p in parts]


def md_tables(text):
    """Yield (heading, header, rows) for every markdown table. The header is the first
    row with two or more non-empty cells (converted sheets start with title rows)."""
    heading = ""
    block = []
    def flush():
        rows = [r for r in (split_row(l) for l in block) if r is not None]
        rows = [r for r in rows if not all(re.fullmatch(r"-{3,}|:?-+:?", c or "---") for c in r)]
        hdr_i = next((i for i, r in enumerate(rows) if sum(1 for c in r if c) >= 2), None)
        if hdr_i is None:
            return None
        return (heading, rows[hdr_i], rows[hdr_i + 1:])
    for line in text.splitlines():
        if line.lstrip().startswith("|"):
            block.append(line)
            continue
        if block:
            t = flush()
            if t:
                yield t
            block = []
        if line.startswith("#"):
            heading = line.lstrip("#").strip()
    if block:
        t = flush()
        if t:
            yield t


def sheet(text, name):
    """Rows of the first table under '## Sheet: <name>' as dicts keyed by header."""
    for heading, hdr, rows in md_tables(text):
        if heading == f"Sheet: {name}":
            return [dict(zip(hdr, r + [""] * (len(hdr) - len(r)))) for r in rows]
    return []


def tables_under(text, heading_prefix):
    out = []
    for heading, hdr, rows in md_tables(text):
        if heading.startswith(heading_prefix):
            out.append((heading, hdr, [dict(zip(hdr, r + [""] * (len(hdr) - len(r)))) for r in rows]))
    return out


class Sources:
    def __init__(self, root, cache, converter=None):
        self.root = Path(root)
        self.cache = Path(cache)
        self.cache.mkdir(parents=True, exist_ok=True)
        self.converter = converter or str(self.root / "22 Microservice Realignment/compat/convert_sources.py")
        self._t = {}
        self.unread = []

    def path(self, rel):
        return self.root / rel

    def converted(self, key):
        if key in self._t:
            return self._t[key]
        rel = SOURCES[key]
        src = self.root / rel
        out = self.cache / (Path(rel).stem + ".md")
        stale = out.exists() and src.exists() and src.stat().st_mtime > out.stat().st_mtime
        if not out.exists() or out.stat().st_size == 0 or stale:
            if not src.exists():
                self.unread.append(f"{rel} (missing)")
                self._t[key] = ""
                return ""
            r = subprocess.run([sys.executable, "-I", self.converter, str(src), str(self.cache)],
                               capture_output=True, text=True, cwd=str(self.root))
            if not out.exists():
                self.unread.append(f"{rel} (convert failed: {r.stderr.strip()[:200]})")
                self._t[key] = ""
                return ""
        self._t[key] = out.read_text(encoding="utf-8", errors="replace")
        return self._t[key]

    def text(self, key):
        if key in self._t:
            return self._t[key]
        p = self.root / TEXT[key]
        try:
            t = p.read_text(encoding="utf-8", errors="replace")
        except OSError:
            self.unread.append(f"{TEXT[key]} (missing)")
            t = ""
        self._t[key] = t
        return t

    # ---- typed views -------------------------------------------------------------
    def lov(self):
        if "_lov" not in self._t:
            t = self.converted("refdata")
            lists = {r["List"]: r for r in sheet(t, "Lists") if r.get("List", "").startswith("LOV-")}
            vals = {}
            for r in sheet(t, "Values"):
                if r.get("List", "").startswith("LOV-"):
                    vals.setdefault(r["List"], []).append((r.get("Code", ""), r.get("English label", "")))
            self._t["_lov"] = (lists, vals)
        return self._t["_lov"]

    def case_model(self):
        t = self.converted("casemodel")
        return sheet(t, "Case status"), sheet(t, "Status transitions")

    def ldm_fields(self, prev=False):
        k = "_ldmp" if prev else "_ldm"
        if k not in self._t:
            t = self.converted("ldm_prev" if prev else "ldm")
            self._t[k] = sheet(t, "Fields")
        return self._t[k]

    def known_names(self):
        """Every field, entity and source-field name in LDM v9 and Data Classification v5."""
        if "_names" not in self._t:
            names = set()
            for r in self.ldm_fields():
                names.update({r.get("Field", ""), r.get("Entity", "")})
                for sf in re.split(r"[ ,;.()]+", r.get("Source field", "")):
                    names.add(sf)
            for r in sheet(self.converted("dclass"), "Fields"):
                names.update({r.get("Field", ""), r.get("Entity", "")})
            names.discard("")
            self._t["_names"] = names
        return self._t["_names"]

    def messages(self):
        if "_msg" not in self._t:
            m = {}
            for heading, hdr, rows in md_tables(self.converted("msgstd")):
                if "ID" in hdr and "English" in hdr:
                    for r in rows:
                        d = dict(zip(hdr, r))
                        if d.get("ID", "").startswith("MSG-"):
                            m[d["ID"]] = d
            self._t["_msg"] = m
        return self._t["_msg"]

    def test_cases(self):
        if "_tc" not in self._t:
            self._t["_tc"] = {r["Test case"]: r for r in sheet(self.converted("tc"), "Story test cases")
                              if r.get("Test case", "").startswith("TC-")}
        return self._t["_tc"]

    def rtm(self):
        if "_rtm" not in self._t:
            out = {}
            for heading, hdr, rows in md_tables(self.converted("rtm")):
                if heading != "Sheet: RTM":
                    continue
                for r in rows:
                    if r and r[0].startswith("REQ-"):
                        out[r[0]] = r
            self._t["_rtm"] = out
        return self._t["_rtm"]

    def decisions(self):
        t = self.converted("declog")
        return sheet(t, "Decisions taken"), sheet(t, "Open decisions")

    def kafka_events(self):
        return [r for r in sheet(self.converted("kafka"), "Events") if r.get("Event type (ce_type)")]

    def temporal(self):
        t = self.converted("temporal")
        return sheet(t, "Workflows"), sheet(t, "Activities"), sheet(t, "Platform rules")

    def params(self):
        p = self.root / TEXT["params"]
        if not p.exists() or p.stat().st_size == 0:
            return None
        with p.open(encoding="utf-8", errors="replace") as f:
            rows = list(csv.reader(f))
        return {r[0] for r in rows[1:] if r}

    def api(self):
        """service -> {'base': str, 'paths': {path: set(methods)}, 'yaml': text}"""
        if "_api" in self._t:
            return self._t["_api"]
        out = {}
        d = self.root / TEXT["apidir"]
        for p in sorted(d.glob("*.yaml")):
            if p.name.endswith(".asyncapi.yaml") or p.name == "index.yaml":
                continue
            txt = p.read_text(encoding="utf-8", errors="replace")
            m = re.search(r"REST base (/api/recovery/[\w-]+/v1)", txt)
            base = m.group(1) if m else ""
            paths, cur = {}, None
            in_paths = False
            for line in txt.splitlines():
                if re.match(r"^paths:\s*$", line):
                    in_paths = True
                    continue
                if in_paths and re.match(r"^\S", line):
                    in_paths = False
                if in_paths:
                    mp = re.match(r"^  (/\S*):\s*$", line)
                    if mp:
                        cur = mp.group(1)
                        paths[cur] = set()
                        continue
                    mm = re.match(r"^    (get|post|put|patch|delete):", line)
                    if mm and cur:
                        paths[cur].add(mm.group(1).upper())
            out[p.stem] = {"base": base, "paths": paths, "yaml": txt, "file": p.name}
        self._t["_api"] = out
        return out

    def doc_versions(self):
        """Highest version of every 'Recovery Workbench <name> vN' in Document Index v14."""
        if "_ver" not in self._t:
            best = {}
            for m in re.finditer(r"Recovery Workbench ([A-Z][\w ,&()'-]*?) v(\d+)\b", self.text("docindex")):
                n, v = m.group(1).strip(), int(m.group(2))
                best[n] = max(best.get(n, 0), v)
            self._t["_ver"] = best
        return self._t["_ver"]

    def register(self, key):
        """GAP/ASM register rows as dicts."""
        k = "_reg_" + key
        if k not in self._t:
            rows = {}
            for heading, hdr, rs in md_tables(self.text(key)):
                for r in rs:
                    d = dict(zip(hdr, r + [""] * (len(hdr) - len(r))))
                    i = r[0] if r else ""
                    if re.fullmatch(r"(GAP|ASM)-\d{4}", i):
                        rows[i] = d
            self._t[k] = rows
        return self._t[k]

    def story_index(self):
        """story key -> path, from the file names under the story folder."""
        if "_stories" not in self._t:
            idx = {}
            for p in (self.root / TEXT["stories"]).rglob("*.md"):
                key = story_key_from_name(p.name)
                if key:
                    idx.setdefault(key, p)
            self._t["_stories"] = idx
        return self._t["_stories"]


def story_key_from_name(name):
    m = re.match(r"RWB (\w+) (\w+) (APP-\d+|APP|CON|OPS|ITG|DB|INF)\b", name)
    if not m:
        return None
    return f"RWB-{m.group(1)}-{m.group(2)}-{m.group(3)}"
