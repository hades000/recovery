#!/usr/bin/env python3
"""Convert the Recovery Workbench document set into agent-readable Markdown.

Uses only the Python standard library: DOCX, XLSX and PPTX are ZIP+XML packages.
Originals in the twelve source folders are never modified.
"""
from __future__ import annotations

import csv
import hashlib
import io
import json
import posixpath
import re
import zipfile
from datetime import date
from html.parser import HTMLParser
from pathlib import Path
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parents[2]
REPO = ROOT / "13 AI-First SDLC repository"
OUT = REPO / "requirement" / "legacy"
INDEX = ROOT / "12 Project communication" / "Recovery Workbench Document Index v11.md"
TODAY = date.today().isoformat()

NS_W = "http://schemas.openxmlformats.org/wordprocessingml/2006/main"
NS_R = "http://schemas.openxmlformats.org/officeDocument/2006/relationships"
NS_A = "http://schemas.openxmlformats.org/drawingml/2006/main"
NS_P = "http://schemas.openxmlformats.org/presentationml/2006/main"
NS_S = "http://schemas.openxmlformats.org/spreadsheetml/2006/main"
NS_REL = "http://schemas.openxmlformats.org/package/2006/relationships"
W = "{%s}" % NS_W
R = "{%s}" % NS_R
A = "{%s}" % NS_A
P = "{%s}" % NS_P
S = "{%s}" % NS_S
REL = "{%s}" % NS_REL

SKIP_HTML = {"script", "style", "noscript", "svg", "nav", "header", "footer",
             "form", "button", "input", "select", "textarea", "iframe"}


# --------------------------------------------------------------------------- #
# helpers
# --------------------------------------------------------------------------- #
def slug(value: str) -> str:
    value = value.replace("&", " and ")
    value = re.sub(r"[^\w\s.-]", "", value, flags=re.UNICODE)
    value = re.sub(r"[\s_.]+", "-", value.strip())
    value = re.sub(r"-{2,}", "-", value)
    return value.strip("-").lower() or "untitled"


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as fh:
        for chunk in iter(lambda: fh.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def md_escape(text: str) -> str:
    return (text or "").replace("|", "\\|").replace("\r", "").replace("\n", "<br>").strip()


def md_table(rows: list[list[str]]) -> str:
    rows = [[md_escape(c) for c in row] for row in rows if any((c or "").strip() for c in row)]
    if not rows:
        return ""
    width = max(len(r) for r in rows)
    rows = [r + [""] * (width - len(r)) for r in rows]
    out = ["| " + " | ".join(rows[0]) + " |",
           "|" + "|".join(["---"] * width) + "|"]
    for row in rows[1:]:
        out.append("| " + " | ".join(row) + " |")
    return "\n".join(out)


def source_header(src_rel: str, kind: str, note: str = "") -> str:
    extra = f" · {note}" if note else ""
    return (f"<!-- source: {src_rel} -->\n"
            f"<!-- converted: {TODAY} from {kind}{extra} -->\n\n"
            f"> **Source:** `{src_rel}`  \n"
            f"> **Converted from:** {kind}{extra}\n\n")


def write_text(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text.rstrip() + "\n", encoding="utf-8")


def version_of(stem: str) -> str:
    matches = re.findall(r"\bv(\d+(?:\.\d+)?)\b", stem, flags=re.I)
    return matches[-1] if matches else ""


def norm_title(stem: str) -> str:
    s = stem.lower()
    s = re.sub(r"^recovery workbench\s+", "", s)
    s = re.sub(r"\s+v\d+(?:\.\d+)?$", "", s)
    s = re.sub(r"\s+", " ", s)
    s = re.sub(r"[^a-z0-9 ]", "", s)
    return s.strip()


def col_index(ref: str) -> int:
    letters = re.match(r"([A-Z]+)", ref.upper())
    if not letters:
        return 0
    n = 0
    for ch in letters.group(1):
        n = n * 26 + (ord(ch) - 64)
    return n - 1


def parse_ref(ref: str) -> tuple[int, int]:
    m = re.match(r"([A-Z]+)(\d+)", ref.upper())
    if not m:
        return 0, 0
    return int(m.group(2)) - 1, col_index(m.group(1) + "1")


# --------------------------------------------------------------------------- #
# DOCX
# --------------------------------------------------------------------------- #
def docx_paragraph_text(p: ET.Element) -> str:
    parts: list[str] = []
    for node in p.iter():
        if node.tag == f"{W}t":
            parts.append(node.text or "")
        elif node.tag == f"{W}tab":
            parts.append("\t")
        elif node.tag == f"{W}br":
            parts.append("\n")
    return "".join(parts)


def docx_heading_level(style: str) -> int:
    s = (style or "").lower()
    if s in ("title",):
        return 1
    m = re.search(r"heading\s*(\d+)", s)
    if m:
        return min(int(m.group(1)), 6)
    return 0


def docx_table(tbl: ET.Element) -> list[list[str]]:
    rows: list[list[str]] = []
    for tr in tbl.findall(f"{W}tr"):
        cells: list[str] = []
        for tc in tr.findall(f"{W}tc"):
            text = " ".join(docx_paragraph_text(p).strip() for p in tc.findall(f"{W}p"))
            text = re.sub(r"\s+", " ", text).strip()
            span = 1
            tc_pr = tc.find(f"{W}tcPr")
            if tc_pr is not None:
                gs = tc_pr.find(f"{W}gridSpan")
                if gs is not None:
                    try:
                        span = max(1, int(gs.get(f"{W}val", "1")))
                    except ValueError:
                        span = 1
                vm = tc_pr.find(f"{W}vMerge")
                if vm is not None and vm.get(f"{W}val") == "continue":
                    text = ""
            cells.append(text)
            cells.extend([""] * (span - 1))
        rows.append(cells)
    if not rows:
        return rows
    width = max(len(r) for r in rows)
    return [r + [""] * (width - len(r)) for r in rows]


def docx_to_md(path: Path) -> tuple[str, str]:
    with zipfile.ZipFile(path) as z:
        root = ET.fromstring(z.read("word/document.xml"))
        image_count = len([n for n in z.namelist() if n.startswith("word/media/")])
    body = root.find(f"{W}body")
    lines: list[str] = []
    if body is None:
        return "", "no document body"
    for child in body:
        if child.tag == f"{W}p":
            style_el = child.find(f"{W}pPr/{W}pStyle")
            style = style_el.get(f"{W}val", "") if style_el is not None else ""
            text = docx_paragraph_text(child).strip()
            if not text:
                continue
            level = docx_heading_level(style)
            if level:
                lines.append("#" * level + " " + re.sub(r"\s+", " ", text))
            elif child.find(f"{W}pPr/{W}numPr") is not None:
                lines.append("- " + re.sub(r"\s+", " ", text))
            else:
                lines.append(text)
            lines.append("")
        elif child.tag == f"{W}tbl":
            table = md_table(docx_table(child))
            if table:
                lines.append(table)
                lines.append("")
    note = f"{image_count} embedded image(s) not extracted; see original" if image_count else ""
    return "\n".join(lines), note


# --------------------------------------------------------------------------- #
# XLSX
# --------------------------------------------------------------------------- #
def xlsx_shared_strings(z: zipfile.ZipFile) -> list[str]:
    if "xl/sharedStrings.xml" not in z.namelist():
        return []
    root = ET.fromstring(z.read("xl/sharedStrings.xml"))
    values = []
    for si in root.findall(f"{S}si"):
        values.append("".join(t.text or "" for t in si.iter(f"{S}t")))
    return values


def xlsx_rels(z: zipfile.ZipFile, path: str) -> dict[str, str]:
    if path not in z.namelist():
        return {}
    root = ET.fromstring(z.read(path))
    return {rel.get("Id"): rel.get("Target") for rel in root.findall(f"{REL}Relationship")}


def xlsx_sheet(z: zipfile.ZipFile, target: str, shared: list[str]) -> tuple[list[list[str]], list[str]]:
    root = ET.fromstring(z.read(target))
    rows: list[list[str]] = []
    for row in root.findall(f"{S}sheetData/{S}row"):
        cells: dict[int, str] = {}
        for c in row.findall(f"{S}c"):
            idx = col_index(c.get("r", "A1"))
            t = c.get("t", "")
            v = c.find(f"{S}v")
            is_el = c.find(f"{S}is")
            value = ""
            if t == "s" and v is not None:
                try:
                    value = shared[int(v.text or "0")]
                except (ValueError, IndexError):
                    value = ""
            elif t == "inlineStr" and is_el is not None:
                value = "".join(x.text or "" for x in is_el.iter(f"{S}t"))
            elif t == "b" and v is not None:
                value = "TRUE" if (v.text or "") == "1" else "FALSE"
            elif v is not None:
                value = v.text or ""
            elif c.find(f"{S}f") is not None:
                value = ""
            cells[idx] = value
        if cells:
            width = max(cells) + 1
            rows.append([cells.get(i, "") for i in range(width)])
    merges: list[str] = []
    mc = root.find(f"{S}mergeCells")
    if mc is not None:
        for m in mc.findall(f"{S}mergeCell"):
            ref = m.get("ref", "")
            merges.append(ref)
            try:
                a, b = ref.split(":")
                r1, c1 = parse_ref(a)
                r2, c2 = parse_ref(b)
                top = rows[r1][c1] if r1 < len(rows) and c1 < len(rows[r1]) else ""
                for rr in range(r1, min(r2, len(rows) - 1) + 1):
                    while len(rows[rr]) <= c2:
                        rows[rr].append("")
                    for cc in range(c1, c2 + 1):
                        if not rows[rr][cc]:
                            rows[rr][cc] = top
            except Exception:
                continue
    return rows, merges


def xlsx_to_md(path: Path, csv_dir: Path) -> tuple[str, list[Path], str]:
    outputs: list[Path] = []
    with zipfile.ZipFile(path) as z:
        shared = xlsx_shared_strings(z)
        wb = ET.fromstring(z.read("xl/workbook.xml"))
        rels = xlsx_rels(z, "xl/_rels/workbook.xml.rels")
        sheets: list[tuple[str, str]] = []
        for sh in wb.findall(f"{S}sheets/{S}sheet"):
            name = sh.get("name", "Sheet")
            target = rels.get(sh.get(f"{R}id", ""), "")
            if not target:
                continue
            if target.startswith("/"):
                target = target[1:]
            elif not target.startswith("xl/"):
                target = "xl/" + target
            sheets.append((name, target))
        lines: list[str] = []
        for name, target in sheets:
            if target not in z.namelist():
                lines.append(f"## {name}\n\n_Sheet XML not found: {target}_\n")
                continue
            rows, merges = xlsx_sheet(z, target, shared)
            lines.append(f"## {name}")
            lines.append("")
            if merges:
                lines.append(f"_Merged ranges: {', '.join(merges[:40])}"
                             + (" ..." if len(merges) > 40 else "") + "_")
                lines.append("")
            table = md_table(rows)
            lines.append(table if table else "_Empty sheet._")
            lines.append("")
            csv_path = csv_dir / f"{slug(name)}.csv"
            csv_dir.mkdir(parents=True, exist_ok=True)
            with csv_path.open("w", newline="", encoding="utf-8-sig") as fh:
                writer = csv.writer(fh)
                writer.writerows(rows)
            outputs.append(csv_path)
    note = f"{len(sheets)} sheet(s); CSV copies written" if sheets else "no sheets"
    return "\n".join(lines), outputs, note


# --------------------------------------------------------------------------- #
# PPTX
# --------------------------------------------------------------------------- #
def pptx_slide_text(root: ET.Element) -> tuple[str, list[str]]:
    title = ""
    texts: list[str] = []
    for sp in root.iter(f"{P}sp"):
        ph = sp.find(f"{P}nvSpPr/{P}nvPr/{P}ph")
        is_title = ph is not None and ph.get("type") in ("title", "ctrTitle")
        text = " ".join(x.text or "" for x in sp.iter(f"{A}t")).strip()
        if not text:
            continue
        if is_title and not title:
            title = text
        else:
            texts.append(text)
    return title, texts


def pptx_to_md(path: Path) -> tuple[str, str]:
    with zipfile.ZipFile(path) as z:
        pres = ET.fromstring(z.read("ppt/presentation.xml"))
        rels = xlsx_rels(z, "ppt/_rels/presentation.xml.rels")
        slides: list[str] = []
        for sld in pres.findall(f"{P}sldIdLst/{P}sldId"):
            target = rels.get(sld.get(f"{R}id", ""), "")
            if not target:
                continue
            if not target.startswith("ppt/"):
                target = "ppt/" + target
            slides.append(target)
        lines: list[str] = []
        for i, target in enumerate(slides, 1):
            if target not in z.namelist():
                continue
            root = ET.fromstring(z.read(target))
            title, texts = pptx_slide_text(root)
            lines.append(f"## Slide {i}" + (f": {title}" if title else ""))
            lines.append("")
            for text in texts:
                lines.append(text)
                lines.append("")
            for tbl in root.iter(f"{A}tbl"):
                rows = []
                for tr in tbl.findall(f"{A}tr"):
                    row = []
                    for tc in tr.findall(f"{A}tc"):
                        row.append(" ".join(x.text or "" for x in tc.iter(f"{A}t")).strip())
                    rows.append(row)
                table = md_table(rows)
                if table:
                    lines.append(table)
                    lines.append("")
            # notes via slide relationships
            rel_path = target.replace("ppt/slides/", "ppt/slides/_rels/") + ".rels"
            if rel_path in z.namelist():
                srels = xlsx_rels(z, rel_path)
                for rid, ntarget in srels.items():
                    if "notesSlide" not in (ntarget or ""):
                        continue
                    resolved = posixpath.normpath(posixpath.join("ppt/slides", ntarget))
                    if resolved in z.namelist():
                        nroot = ET.fromstring(z.read(resolved))
                        ntext = " ".join(x.text or "" for x in nroot.iter(f"{A}t")).strip()
                        if ntext:
                            lines.append(f"> Notes: {ntext}")
                            lines.append("")
        image_count = len([n for n in z.namelist() if n.startswith("ppt/media/")])
    note = f"{len(slides)} slide(s); {image_count} image(s) not extracted" if slides else "no slides"
    return "\n".join(lines), note


# --------------------------------------------------------------------------- #
# HTML
# --------------------------------------------------------------------------- #
class HtmlToMd(HTMLParser):
    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.lines: list[str] = []
        self.buf: list[str] = []
        self.skip = 0
        self.table: list[list[str]] | None = None
        self.row: list[str] | None = None
        self.cell: list[str] | None = None
        self.pre = False

    def emit(self, text: str) -> None:
        if self.cell is not None:
            self.cell.append(text)
        else:
            self.buf.append(text)

    def flush(self) -> None:
        text = re.sub(r"[ \t]+", " ", "".join(self.buf)).strip()
        if text:
            self.lines.append(text)
        self.buf = []

    def handle_starttag(self, tag: str, attrs) -> None:
        tag = tag.lower()
        if tag in SKIP_HTML:
            self.skip += 1
            return
        if self.skip:
            return
        if tag in ("h1", "h2", "h3", "h4", "h5", "h6"):
            self.flush()
            self.emit("#" * int(tag[1]) + " ")
        elif tag == "p":
            self.flush()
        elif tag == "br":
            self.emit("\n")
        elif tag == "li":
            self.flush()
            self.emit("- ")
        elif tag in ("strong", "b"):
            self.emit("**")
        elif tag in ("em", "i"):
            self.emit("*")
        elif tag == "table":
            self.flush()
            self.table = []
        elif tag == "tr" and self.table is not None:
            self.row = []
        elif tag in ("td", "th") and self.row is not None:
            self.cell = []
        elif tag == "pre":
            self.flush()
            self.pre = True
            self.emit("```\n")

    def handle_endtag(self, tag: str) -> None:
        tag = tag.lower()
        if tag in SKIP_HTML:
            self.skip = max(0, self.skip - 1)
            return
        if self.skip:
            return
        if tag in ("h1", "h2", "h3", "h4", "h5", "h6", "p", "li"):
            self.flush()
        elif tag in ("strong", "b"):
            self.emit("**")
        elif tag in ("em", "i"):
            self.emit("*")
        elif tag in ("td", "th") and self.cell is not None:
            text = re.sub(r"\s+", " ", "".join(self.cell)).strip()
            if self.row is not None:
                self.row.append(text)
            self.cell = None
        elif tag == "tr" and self.row is not None and self.table is not None:
            self.table.append(self.row)
            self.row = None
        elif tag == "table" and self.table is not None:
            table = md_table(self.table)
            if table:
                self.lines.append(table)
            self.table = None
        elif tag == "pre":
            self.emit("\n```")
            self.flush()
            self.pre = False

    def handle_data(self, data: str) -> None:
        if self.skip:
            return
        self.emit(data)

    def result(self) -> str:
        self.flush()
        return "\n\n".join(self.lines)


def html_to_md(path: Path) -> tuple[str, str]:
    text = path.read_text(encoding="utf-8", errors="replace")
    parser = HtmlToMd()
    parser.feed(text)
    return parser.result(), "HTML text and tables; styling removed"


# --------------------------------------------------------------------------- #
# index and mapping
# --------------------------------------------------------------------------- #
def parse_index() -> dict[str, tuple[int, str]]:
    mapping: dict[str, tuple[int, str]] = {}
    if not INDEX.exists():
        return mapping
    for line in INDEX.read_text(encoding="utf-8").splitlines():
        if not line.startswith("|"):
            continue
        cells = [c.strip() for c in line.strip().strip("|").split("|")]
        if len(cells) < 5 or not re.fullmatch(r"\d+", cells[0]):
            continue
        doc_no, title, files = int(cells[0]), cells[1], cells[4]
        for name in [x.strip() for x in files.split(",") if x.strip()]:
            mapping[name] = (doc_no, title)
    return mapping


DOC_COPIES = {
    "project overview": "docs/discovery/project-overview.md",
    "business architecture": "docs/discovery/business-architecture.md",
    "user journeys": "docs/discovery/user-journeys.md",
    "case journeys": "docs/discovery/case-journeys.md",
    "target operating model": "docs/discovery/target-operating-model.md",
    "partner operating model": "docs/discovery/partner-operating-model.md",
    "business glossary": "docs/discovery/business-glossary.md",
    "feature list": "docs/discovery/feature-list.md",
    "business measures and targets": "docs/discovery/business-measures.md",
    "stakeholder map and communication plan": "docs/discovery/stakeholder-map.md",
    "lean brd epic 1": "docs/brds/lean-brd-epic-1.md",
    "lean brd epic 2": "docs/brds/lean-brd-epic-2.md",
    "business requirements program": "docs/brds/business-requirements-program.md",
    "business requirements epic 1": "docs/brds/business-requirements-epic-1.md",
    "business requirements epic 2": "docs/brds/business-requirements-epic-2.md",
    "epics 3 to 8 specification": "docs/prds/epics-3-to-8-specification.md",
    "reporting and management information requirements": "docs/prds/reporting-and-mi-requirements.md",
    "non functional specification": "docs/prds/non-functional-specification.md",
    "ace architecture decision": "docs/architecture/decisions/ace-architecture-decision.md",
}

CANONICAL_OVERRIDES = {
    "business rules and routing logic": {".xlsx": "Yes (data)", ".html": "Reference"},
    "case and workflow model": {".xlsx": "Yes (data)", ".html": "Reference"},
    "detailed process flows": {".xlsx": "Yes (data)", ".html": "Reference"},
    "process architecture": {".xlsx": "Yes (data)", ".pptx": "Reference"},
    "target architecture": {".docx": "Yes (narrative)", ".pptx": "Reference"},
    "ai and agent architecture": {".docx": "Yes (narrative)", ".pptx": "Reference"},
    "release plan": {".xlsx": "Yes (data)", ".pptx": "Reference"},
    "run operating model": {".docx": "Yes (narrative)", ".pptx": "Reference"},
    "training and change plan": {".docx": "Yes (narrative)", ".pptx": "Reference"},
    "ways of working and governance": {".docx": "Yes (narrative)", ".pptx": "Reference"},
    "partner operating model": {".docx": "Yes (narrative)", ".pptx": "Reference"},
    "conceptual data model": {".xlsx": "Yes (data)", ".pptx": "Reference"},
    "volume and scale forecast": {".xlsx": "Yes (data)", ".pptx": "Reference"},
    "party and customer master data design": {".docx": "Yes (narrative)", ".xlsx": "Yes (data)"},
    "reporting and management information requirements": {".docx": "Yes (narrative)", ".xlsx": "Yes (data)"},
    "batch and scheduling design": {".docx": "Yes (narrative)", ".xlsx": "Yes (data)"},
    "interface specifications": {".md": "Yes (narrative)", ".xlsx": "Yes (data)"},
    "event and messaging design": {".md": "Yes (narrative)", ".xlsx": "Yes (data)"},
    "agent catalog and specifications": {".md": "Yes (narrative)", ".xlsx": "Yes (data)"},
    "entity relationship diagram": {".html": "Yes", ".pdf": "Reference"},
    "screen specifications": {".md": "Yes", ".html": "Reference"},
    "design system and component library": {".html": "Yes"},
    "project hub": {".html": "Reference only"},
    "user stories epic 1": {".md": "Yes (narrative)", ".xlsx": "Yes (data)", ".zip": "Yes (per-story)"},
    "user stories epic 2": {".md": "Yes (narrative)", ".xlsx": "Yes (data)", ".zip": "Yes (per-story)"},
    "user stories epics 3 to 8": {".md": "Yes (narrative)", ".xlsx": "Yes (data)"},
    "technical specifications by module": {".zip": "Yes (archive)"},
    "functional specifications by module": {".zip": "Yes (archive)"},
    "document index": {".md": "Yes"},
    "document control sheet": {".xlsx": "Yes"},
    "requirements traceability matrix": {".xlsx": "Yes"},
    "physical schema": {".sql": "Yes"},
    "api specification": {".yaml": "Yes", ".html": "Reference"},
}

DEFAULT_RANK = {".md": 6, ".xlsx": 5, ".docx": 4, ".pptx": 3, ".html": 2, ".pdf": 1, ".zip": 7}


def assign_canonical(entries: list[dict]) -> None:
    groups: dict[str, list[dict]] = {}
    for e in entries:
        if e.get("kind") == "zip-entry":
            continue
        groups.setdefault(e["norm_title"], []).append(e)
    for title, group in groups.items():
        override = CANONICAL_OVERRIDES.get(title)
        if override:
            for e in group:
                e["canonical"] = override.get(e["ext"], "Reference")
            continue
        # default: one canonical, others reference/superseded
        group_sorted = sorted(group, key=lambda x: (DEFAULT_RANK.get(x["ext"], 0), x["version"]), reverse=True)
        top = group_sorted[0]
        top["canonical"] = "Yes"
        for e in group_sorted[1:]:
            if e["ext"] == top["ext"] and e["version"] != top["version"]:
                e["canonical"] = "Superseded"
                e["duplicate_of"] = top["source_rel"]
            elif e["ext"] in (".html", ".pdf", ".pptx"):
                e["canonical"] = "Reference"
                e["duplicate_of"] = top["source_rel"]
            else:
                e["canonical"] = "Reference"


def destination_for(entry: dict) -> list[str]:
    dests = [entry["legacy_dest"]]
    if entry.get("kind") == "zip-entry":
        name = Path(entry["entry_name"]).stem
        if name.lower().startswith("recovery workbench fsd"):
            dests.append(f"docs/prds/{slug(name)}.md")
        return dests
    title = entry["norm_title"]
    if title in DOC_COPIES:
        dests.append(DOC_COPIES[title])
    return dests


# --------------------------------------------------------------------------- #
# processing
# --------------------------------------------------------------------------- #
def process_file(path: Path, folder_slug: str, index_map: dict, entries: list[dict],
                 failures: list[str]) -> None:
    rel = path.relative_to(ROOT).as_posix()
    ext = path.suffix.lower()
    stem = path.stem
    base = OUT / folder_slug / slug(stem)
    if ext == ".md":
        legacy_dest = base.with_suffix(".md")
    elif ext in (".docx", ".xlsx", ".pptx", ".html"):
        legacy_dest = base.parent / f"{slug(stem)}-{ext[1:]}.md"
    else:
        legacy_dest = base.with_suffix(ext)
    legacy_dest = legacy_dest.relative_to(REPO).as_posix()
    doc_no, doc_title = index_map.get(path.name, ("", ""))
    entry = {
        "source_rel": rel,
        "source_name": path.name,
        "folder": folder_slug,
        "ext": ext,
        "bytes": path.stat().st_size,
        "sha256": sha256(path),
        "doc_no": doc_no,
        "doc_title": doc_title,
        "title": stem,
        "version": version_of(stem),
        "norm_title": norm_title(stem),
        "kind": "file",
        "legacy_dest": legacy_dest,
        "outputs": [],
        "conversion": "pending",
        "canonical": "",
        "duplicate_of": "",
        "notes": "",
    }
    entries.append(entry)

    if ext == ".md":
        text = path.read_text(encoding="utf-8", errors="replace")
        write_text(REPO / legacy_dest, source_header(rel, "Markdown (copied)") + text)
        entry["conversion"] = "copied"
        entry["outputs"].append(legacy_dest)
    elif ext == ".docx":
        try:
            body, note = docx_to_md(path)
            write_text(REPO / legacy_dest, source_header(rel, "DOCX") + body)
            entry["conversion"] = "converted"
            entry["notes"] = note
            entry["outputs"].append(legacy_dest)
        except Exception as exc:
            entry["conversion"] = "failed"
            entry["notes"] = str(exc)
            failures.append(f"{rel}: {exc}")
    elif ext == ".xlsx":
        try:
            body, csv_outputs, note = xlsx_to_md(path, OUT / folder_slug / "_csv" / slug(stem))
            write_text(REPO / legacy_dest, source_header(rel, "XLSX") + body)
            entry["conversion"] = "converted"
            entry["notes"] = note
            entry["outputs"].append(legacy_dest)
            for csv_path in csv_outputs:
                entry["outputs"].append(csv_path.relative_to(REPO).as_posix())
        except Exception as exc:
            entry["conversion"] = "failed"
            entry["notes"] = str(exc)
            failures.append(f"{rel}: {exc}")
    elif ext == ".pptx":
        try:
            body, note = pptx_to_md(path)
            write_text(REPO / legacy_dest, source_header(rel, "PPTX") + body)
            entry["conversion"] = "converted"
            entry["notes"] = note
            entry["outputs"].append(legacy_dest)
        except Exception as exc:
            entry["conversion"] = "failed"
            entry["notes"] = str(exc)
            failures.append(f"{rel}: {exc}")
    elif ext == ".html":
        if "project hub" in stem.lower():
            entry["conversion"] = "skipped"
            entry["canonical"] = "Reference only"
            entry["notes"] = "26 MB generated single-page app; indexed as reference, not converted"
        else:
            try:
                body, note = html_to_md(path)
                write_text(REPO / legacy_dest, source_header(rel, "HTML") + body)
                entry["conversion"] = "converted"
                entry["notes"] = note
                entry["outputs"].append(legacy_dest)
            except Exception as exc:
                entry["conversion"] = "failed"
                entry["notes"] = str(exc)
                failures.append(f"{rel}: {exc}")
    elif ext == ".zip":
        entry["conversion"] = "extracted"
        entry["canonical"] = "Yes (archive)"
        zip_out = OUT / folder_slug / (slug(stem) + "_extracted")
        try:
            with zipfile.ZipFile(path) as z:
                for info in z.infolist():
                    if info.is_dir():
                        continue
                    target = zip_out / info.filename
                    target.parent.mkdir(parents=True, exist_ok=True)
                    with z.open(info) as src, target.open("wb") as dst:
                        dst.write(src.read())
                    zrel = f"{rel}!{info.filename}"
                    zext = target.suffix.lower()
                    zbase = zip_out / Path(info.filename).stem
                    if zext == ".md":
                        zlegacy_path = zbase.with_suffix(".md")
                    elif zext in (".docx", ".xlsx", ".pptx", ".html"):
                        zlegacy_path = zbase.parent / f"{slug(Path(info.filename).stem)}-{zext[1:]}.md"
                    else:
                        zlegacy_path = zbase.with_suffix(zext)
                    zlegacy = zlegacy_path.relative_to(REPO).as_posix()
                    zentry = {
                        "source_rel": zrel,
                        "source_name": Path(info.filename).name,
                        "folder": folder_slug,
                        "ext": zext,
                        "bytes": info.file_size,
                        "sha256": hashlib.sha256(z.read(info)).hexdigest(),
                        "doc_no": index_map.get(Path(info.filename).name, ("", ""))[0],
                        "doc_title": index_map.get(Path(info.filename).name, ("", ""))[1],
                        "title": Path(info.filename).stem,
                        "version": version_of(Path(info.filename).stem),
                        "norm_title": norm_title(Path(info.filename).stem),
                        "kind": "zip-entry",
                        "container": rel,
                        "entry_name": info.filename,
                        "legacy_dest": zlegacy,
                        "outputs": [],
                        "conversion": "pending",
                        "canonical": "Yes (per-story)" if "story files" in stem.lower() else "Yes (extracted)",
                        "duplicate_of": "",
                        "notes": "",
                    }
                    entries.append(zentry)
                    if zext == ".md":
                        text = target.read_text(encoding="utf-8", errors="replace")
                        write_text(REPO / zlegacy, source_header(zrel, "Markdown (extracted)") + text)
                        zentry["conversion"] = "extracted"
                        zentry["outputs"].append(zlegacy)
                    elif zext == ".docx":
                        body, note = docx_to_md(target)
                        write_text(REPO / zlegacy, source_header(zrel, "DOCX (extracted)") + body)
                        zentry["conversion"] = "converted"
                        zentry["notes"] = note
                        zentry["outputs"].append(zlegacy)
                    elif zext == ".xlsx":
                        body, csv_outputs, note = xlsx_to_md(target, zip_out / "_csv" / slug(Path(info.filename).stem))
                        write_text(REPO / zlegacy, source_header(zrel, "XLSX (extracted)") + body)
                        zentry["conversion"] = "converted"
                        zentry["notes"] = note
                        zentry["outputs"].append(zlegacy)
                        for csv_path in csv_outputs:
                            zentry["outputs"].append(csv_path.relative_to(REPO).as_posix())
                    elif zext == ".pptx":
                        body, note = pptx_to_md(target)
                        write_text(REPO / zlegacy, source_header(zrel, "PPTX (extracted)") + body)
                        zentry["conversion"] = "converted"
                        zentry["notes"] = note
                        zentry["outputs"].append(zlegacy)
                    elif zext == ".html":
                        body, note = html_to_md(target)
                        write_text(REPO / zlegacy, source_header(zrel, "HTML (extracted)") + body)
                        zentry["conversion"] = "converted"
                        zentry["notes"] = note
                        zentry["outputs"].append(zlegacy)
                    else:
                        zentry["conversion"] = "copied"
                        zentry["outputs"].append(zlegacy)
        except Exception as exc:
            entry["conversion"] = "failed"
            entry["notes"] = str(exc)
            failures.append(f"{rel}: {exc}")
    elif ext in (".sql", ".yaml", ".yml"):
        target = REPO / legacy_dest
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_bytes(path.read_bytes())
        entry["conversion"] = "copied"
        entry["outputs"].append(legacy_dest)
    elif ext == ".pdf":
        entry["conversion"] = "skipped"
        entry["notes"] = "PDF duplicate; HTML/SQL equivalent retained"
    else:
        entry["conversion"] = "unsupported"
        entry["notes"] = "No converter for this format"


def split_adrs(entry: dict, failures: list[str]) -> None:
    if entry["norm_title"] != "architecture decision records" or entry["conversion"] != "copied":
        return
    src = REPO / entry["legacy_dest"]
    text = src.read_text(encoding="utf-8")
    parts = re.split(r"(?m)^## (ADR-\d+ .+)$", text)
    if len(parts) < 3:
        return
    out_dir = REPO / "docs" / "architecture" / "decisions"
    out_dir.mkdir(parents=True, exist_ok=True)
    created = []
    for i in range(1, len(parts), 2):
        heading = parts[i].strip()
        body = parts[i + 1].strip()
        m = re.match(r"(ADR-\d+)\s+(.+)", heading)
        if not m:
            continue
        adr_id, title = m.group(1), m.group(2)
        dest = out_dir / f"{adr_id.lower()}-{slug(title)}.md"
        write_text(dest, f"<!-- source: {entry['source_rel']} -->\n\n# {heading}\n\n{body}\n")
        created.append(dest.relative_to(REPO).as_posix())
    entry["outputs"].extend(created)
    entry["notes"] = (entry["notes"] + "; " if entry["notes"] else "") + f"split into {len(created)} ADR files"


def copy_doc_copies(entries: list[dict]) -> None:
    by_dest: dict[str, list[dict]] = {}
    for entry in entries:
        for dest in destination_for(entry)[1:]:
            if dest.endswith(".md"):
                by_dest.setdefault(dest, []).append(entry)
    rank = {".md": 6, ".docx": 5, ".xlsx": 4, ".pptx": 3, ".html": 2}
    for dest, candidates in sorted(by_dest.items()):
        usable = [c for c in candidates
                  if c.get("canonical") not in ("Reference", "Reference only", "Superseded", "Duplicate")]
        if not usable:
            continue
        entry = max(usable, key=lambda c: (rank.get(c["ext"], 0), c["version"]))
        src = REPO / entry["legacy_dest"]
        if not src.exists():
            continue
        header = (f"<!-- working-copy-of: {entry['legacy_dest']} -->\n"
                  f"> **Working copy.** Canonical source: `{entry['legacy_dest']}`. "
                  f"Edit the source, not this copy.\n\n")
        text = src.read_text(encoding="utf-8")
        text = re.sub(r"^<!-- source:.*?-->\n<!-- converted:.*?-->\n\n> \*\*Source:\*\*.*?\n\n", "", text, flags=re.S)
        write_text(REPO / dest, header + text)
        entry["outputs"].append(dest)


def write_map(entries: list[dict], failures: list[str]) -> None:
    by_folder: dict[str, list[dict]] = {}
    for e in entries:
        by_folder.setdefault(e["folder"], []).append(e)
    lines = ["# Recovery Workbench document map", "",
             f"Generated {TODAY} from the twelve source folders. "
             "Every source file is listed with its toolkit destination and lifecycle phase.", "",
             "## How to read this map", "",
             "| Column | Meaning |", "|---|---|",
             "| Source | Path in the original SharePoint set |",
             "| Doc # | Number in the Document Index v11 (blank when not listed) |",
             "| Canonical | `Yes` = use this version; `Yes (data)` / `Yes (narrative)` = complementary canonical copies; `Reference` = read-only context; `Superseded` = older version; `Duplicate` = same content elsewhere |",
             "| Duplicate of | The canonical file when this row is a duplicate or reference |",
             "| Destination(s) | `requirement/legacy/...` is the agent corpus; `docs/...` is a working copy for a lifecycle phase |",
             "| Phase | Playbook lifecycle phase (0–10) |",
             "| Conversion | `copied`, `converted`, `extracted`, `skipped`, `unsupported`, `failed` |", "",
             "## Summary", "",
             "| Source folder | Files | Converted | Copied | Extracted | Skipped | Failed |",
             "|---|---:|---:|---:|---:|---:|---:|"]
    for folder in sorted(by_folder):
        rows = by_folder[folder]
        def count(kind: str) -> int:
            return sum(1 for r in rows if r["conversion"] == kind)
        lines.append(f"| {folder} | {len(rows)} | {count('converted')} | {count('copied')} | "
                     f"{count('extracted')} | {count('skipped')} | {count('failed')} |")
    lines += ["", "## Files", ""]
    for folder in sorted(by_folder):
        lines.append(f"### {folder}")
        lines.append("")
        lines.append("| Map ID | Source | Doc # | Title | Ver | Format | Canonical | Duplicate of | Destination(s) | Phase | Conversion | Notes |")
        lines.append("|---|---|---|---|---|---|---|---|---|---|---|---|")
        for i, e in enumerate(sorted(by_folder[folder], key=lambda x: x["source_rel"]), 1):
            dests = "<br>".join(f"`{d}`" for d in destination_for(e))
            dup = f"`{e['duplicate_of']}`" if e["duplicate_of"] else ""
            notes = (e["notes"] or "").replace("|", "\\|")
            lines.append(f"| {folder[:2]}-{i:03d} | `{e['source_rel']}` | {e['doc_no']} | "
                         f"{e['title']} | {e['version']} | {e['ext']} | {e['canonical']} | {dup} | "
                         f"{dests} |  | {e['conversion']} | {notes} |")
        lines.append("")
    lines += ["## Failures", ""]
    if failures:
        lines += [f"- {f}" for f in failures]
    else:
        lines.append("None.")
    lines.append("")
    write_text(OUT / "DOCUMENT_MAP.md", "\n".join(lines))


def write_report(entries: list[dict], failures: list[str]) -> None:
    total = len(entries)
    counts: dict[str, int] = {}
    exts: dict[str, int] = {}
    for e in entries:
        counts[e["conversion"]] = counts.get(e["conversion"], 0) + 1
        exts[e["ext"]] = exts.get(e["ext"], 0) + 1
    lines = ["# Conversion report", "", f"Run: {TODAY}", "",
             f"Source files and zip entries: **{total}**", "",
             "## By conversion status", "", "| Status | Count |", "|---|---:|"]
    for k in sorted(counts):
        lines.append(f"| {k} | {counts[k]} |")
    lines += ["", "## By format", "", "| Format | Count |", "|---|---:|"]
    for k in sorted(exts):
        lines.append(f"| {k or '(none)'} | {exts[k]} |")
    lines += ["", "## Failures", ""]
    lines += [f"- {f}" for f in failures] if failures else ["None."]
    lines += ["", "## Known limits", "",
              "- DOCX/PPTX images are counted but not extracted; originals remain in the source folders.",
              "- XLSX cells use cached values; formulas without a cached value are blank.",
              "- Merged XLSX cells are filled from the top-left value for readability.",
              "- HTML conversion keeps text and tables; styling, scripts and navigation are removed.",
              "- The 26 MB Project Hub is indexed as reference only and is not converted.",
              "- PDF files are skipped where an HTML or SQL equivalent exists.",
              "", "## Spot checks", "",
              "Open one converted file per format and compare headings, table row counts and Thai text with the original:",
              "", "- DOCX: `requirement/legacy/05-technical-architecture/...target-architecture...md`",
              "- XLSX: `requirement/legacy/06-data/...logical-data-model...md`",
              "- PPTX: `requirement/legacy/02-business-architecture-and-process/...business-architecture...md`",
              "- HTML: `requirement/legacy/02-business-architecture-and-process/...business-rules-and-routing-logic...md`",
              "- ZIP: `requirement/legacy/04-user-stories/...story-files..._extracted/`"]
    write_text(OUT / "_conversion-report.md", "\n".join(lines))


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    index_map = parse_index()
    entries: list[dict] = []
    failures: list[str] = []
    source_folders = sorted([p for p in ROOT.iterdir()
                             if p.is_dir() and re.match(r"^(0[1-9]|1[0-2]) ", p.name)])
    for folder in source_folders:
        folder_slug = slug(folder.name)
        for path in sorted(folder.rglob("*")):
            if not path.is_file():
                continue
            if path.name.startswith(".~lock.") or path.name.startswith("~$"):
                continue
            if path.name in (".DS_Store", "Thumbs.db"):
                continue
            process_file(path, folder_slug, index_map, entries, failures)
    assign_canonical(entries)
    for entry in entries:
        split_adrs(entry, failures)
    copy_doc_copies(entries)
    write_map(entries, failures)
    write_report(entries, failures)
    manifest = [{k: v for k, v in e.items() if k not in ("norm_title",)} for e in entries]
    write_text(OUT / "_manifest.json", json.dumps(manifest, indent=2, ensure_ascii=False))
    print(f"Processed {len(entries)} files/entries; {len(failures)} failures")
    print(f"Output: {OUT}")


if __name__ == "__main__":
    main()
