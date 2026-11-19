#!/usr/bin/env python3
"""Build the Epic 1 story mind maps as Excalidraw files.

One map per story file, all from the same template, so a reader who has read
one map can read them all.  Usage:

    python build_story_maps.py              # every spec + the overview
    python build_story_maps.py RWB-E1-069   # one story

Standard library only.  Every defect is reported as
``<KEY>.<field>: <problem>`` and the process exits non-zero.
"""

from __future__ import annotations

import json
import math
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
OUT = HERE.parent
ROOT = HERE.parents[2]
SPECS = HERE / "specs"

# ---------------------------------------------------------------- palette ---
HERO_FILL, HERO_STROKE = "#3b82f6", "#1e3a5f"
ACE_FILL, ACE_STROKE = "#93c5fd", "#1e3a5f"
ACE_OFF_FILL, ACE_OFF_STROKE = "#dbeafe", "#1e40af"
B_FILL, B_STROKE = "#fef3c7", "#b45309"
TRIG_FILL, TRIG_STROKE = "#fed7aa", "#c2410c"
REC_FILL, REC_STROKE = "#a7f3d0", "#047857"
FN_FILL, FN_STROKE = "#60a5fa", "#1e3a5f"
AI_FILL, AI_STROKE = "#ddd6fe", "#6d28d9"
RULE_FILL, RULE_STROKE = "#fef3c7", "#b45309"
RISK_FILL, RISK_STROKE = "#fee2e2", "#dc2626"
STORE_FILL, STORE_STROKE = "#dbeafe", "#1e40af"
OUT_FILL, OUT_STROKE = "#a7f3d0", "#047857"
EX_FILL = "#1e293b"
EX_HEAD, EX_BODY = "#ffffff", "#22c55e"
T_TITLE, T_SUB, T_DETAIL, T_BODY = "#1e40af", "#3b82f6", "#64748b", "#374151"
T_ON_DARK = "#ffffff"

STATUS = {
    "READY": ("#a7f3d0", "#047857"),
    "PARTIAL": ("#fef3c7", "#b45309"),
    "RETIRED": ("#fecaca", "#b91c1c"),
}

# ---------------------------------------------------------------- limits ----
LIMITS = {
    "title": 66,
    "status_text": 56,
    "goal": 110,
    "why": 180,
    "triggers": 4,
    "ace": 8,
    "writes": 5,
    "reads": 5,
    "stores": 210,
    "functions": 6,
    "rules": 4,
    "risks": 3,
    "example": 8,
    "overview_label": 30,
}
THEMES = ("default", "ai")
TRIGGER_TAGS = ("WHO", "API", "JOB", "EVENT", "BUILD", "LOAD", "CALL", "GATE")
PATH_KINDS = ("trigger", "function", "ace", "table", "store", "ai", "check", "out")

# The longest Flyway file name (V0001__rwb_e1_001_recovery_schema, 35 chars)
# sets the name limit: two columns 380 px apart stay clear at font 16.
NAME_LIMIT = 36


# ------------------------------------------------------------- factories ----
class Doc:
    """One Excalidraw drawing: element list, id set and a deterministic seed."""

    def __init__(self, index: int) -> None:
        self.index = index
        self.els: list[dict] = []
        self.n = 0
        self.ids: set[str] = set()

    def _seed(self) -> int:
        self.n += 1
        return self.index * 1000 + self.n

    def _add(self, el: dict) -> dict:
        if el["id"] in self.ids:
            raise AssertionError(f"duplicate element id {el['id']}")
        self.ids.add(el["id"])
        self.els.append(el)
        return el

    def _base(self, id_: str, type_: str, x: float, y: float, w: float, h: float,
              stroke: str, fill: str, sw: int = 1, dashed: bool = False,
              roundness: dict | None = None) -> dict:
        seed = self._seed()
        return {
            "id": id_,
            "type": type_,
            "x": x,
            "y": y,
            "width": w,
            "height": h,
            "angle": 0,
            "strokeColor": stroke,
            "backgroundColor": fill,
            "fillStyle": "solid",
            "strokeWidth": sw,
            "strokeStyle": "dashed" if dashed else "solid",
            "roughness": 0,
            "opacity": 100,
            "groupIds": [],
            "frameId": None,
            "roundness": roundness,
            "seed": seed,
            "version": 1,
            "versionNonce": seed + 500000,
            "isDeleted": False,
            "boundElements": [],
            "updated": 1,
            "link": None,
            "locked": False,
        }

    # -- text ---------------------------------------------------------------
    def text(self, id_: str, x: float, y: float, s: str, fs: int, color: str,
             align: str = "left") -> dict:
        lines = s.split("\n")
        w = math.ceil(max(len(line) for line in lines) * fs * 0.6) + 2
        h = math.ceil(len(lines) * fs * 1.25)
        el = self._base(id_, "text", x, y, w, h, color, "transparent")
        el.update({
            "text": s,
            "originalText": s,
            "fontSize": fs,
            "fontFamily": 3,
            "textAlign": align,
            "verticalAlign": "top",
            "containerId": None,
            "lineHeight": 1.25,
            "autoResize": True,
        })
        return self._add(el)

    def wrapped_text(self, id_: str, x: float, y: float, s: str, fs: int,
                     color: str, chars: int) -> dict:
        return self.text(id_, x, y, "\n".join(greedy_wrap(s, chars)), fs, color)

    def bound_text(self, shape: dict, s: str, fs: int, color: str,
                   chars: int) -> dict:
        return self.bound_lines(shape, greedy_wrap(s, chars), fs, color)

    def bound_lines(self, shape: dict, lines: list[str], fs: int,
                    color: str) -> dict:
        body = "\n".join(lines)
        w = shape["width"] - 20
        h = math.ceil(len(lines) * fs * 1.25)
        x = shape["x"] + 10
        y = shape["y"] + (shape["height"] - h) / 2
        el = self._base(f"{shape['id']}_txt", "text", x, y, w, h, color,
                        "transparent")
        el.update({
            "text": body,
            "originalText": body,
            "fontSize": fs,
            "fontFamily": 3,
            "textAlign": "center",
            "verticalAlign": "middle",
            "containerId": shape["id"],
            "lineHeight": 1.25,
            "autoResize": True,
        })
        self._add(el)
        shape["boundElements"].append({"id": el["id"], "type": "text"})
        return el

    def fit_text(self, shape: dict, s: str, fs: int, color: str, chars: int,
                 min_fs: int = 12, max_lines: int | None = None) -> dict:
        """Bound text that shrinks the font until it fits its shape."""
        size = fs
        while True:
            lines = greedy_wrap(s, chars, break_long=False)
            widest = max(len(line) for line in lines) * size * 0.6
            too_wide = widest > shape["width"] - 20
            too_tall = len(lines) * size * 1.25 > shape["height"] - 6
            too_many = max_lines is not None and len(lines) > max_lines
            if (not too_wide and not too_tall and not too_many) or size <= min_fs:
                return self.bound_lines(shape, lines, size, color)
            size -= 1
            chars = max(8, int(chars * fs / size))

    # -- shapes -------------------------------------------------------------
    def rect(self, id_: str, x: float, y: float, w: float, h: float, fill: str,
             stroke: str, sw: int = 1, dashed: bool = False) -> dict:
        return self._add(self._base(id_, "rectangle", x, y, w, h, stroke, fill,
                                    sw, dashed, {"type": 3}))

    def ellipse(self, id_: str, x: float, y: float, w: float, h: float,
                fill: str, stroke: str, sw: int = 1,
                dashed: bool = False) -> dict:
        return self._add(self._base(id_, "ellipse", x, y, w, h, stroke, fill,
                                    sw, dashed, {"type": 2}))

    def dot(self, id_: str, x: float, y: float, d: float, fill: str,
            stroke: str) -> dict:
        return self._add(self._base(id_, "ellipse", x, y, d, d, stroke, fill))

    # -- connectors ---------------------------------------------------------
    def line(self, id_: str, x: float, y: float, points: list, color: str,
             w: int = 2, dashed: bool = False) -> dict:
        width = max(abs(px) for px, _ in points)
        height = max(abs(py) for _, py in points)
        el = self._base(id_, "line", x, y, width, height, color, "transparent",
                        w, dashed)
        el["points"] = [list(p) for p in points]
        return self._add(el)

    def arrow(self, id_: str, x: float, y: float, points: list, color: str,
              w: int = 2, start: str | None = None, end: str | None = "arrow",
              sb: dict | None = None, eb: dict | None = None,
              dashed: bool = False) -> dict:
        width = max(abs(px) for px, _ in points)
        height = max(abs(py) for _, py in points)
        el = self._base(id_, "arrow", x, y, width, height, color, "transparent",
                        w, dashed)
        el.update({
            "points": [list(p) for p in points],
            "startBinding": binding(sb),
            "endBinding": binding(eb),
            "startArrowhead": start,
            "endArrowhead": end,
            "elbowed": False,
        })
        self._add(el)
        for shape in (sb, eb):
            if shape is not None:
                shape["boundElements"].append({"id": id_, "type": "arrow"})
        return el


def binding(shape: dict | None) -> dict | None:
    if shape is None:
        return None
    return {"elementId": shape["id"], "focus": 0, "gap": 4}


def greedy_wrap(s: str, chars: int, break_long: bool = True) -> list[str]:
    """Wrap at spaces; break a token longer than the limit only if asked."""
    out: list[str] = []
    for para in s.split("\n"):
        line = ""
        for word in para.split(" "):
            if break_long:
                while len(word) > chars:
                    if line:
                        out.append(line)
                        line = ""
                    out.append(word[:chars])
                    word = word[chars:]
            candidate = word if not line else f"{line} {word}"
            if len(candidate) <= chars:
                line = candidate
            else:
                if line:
                    out.append(line)
                line = word
        out.append(line)
    return [line for line in out if line != ""] or [""]


# --------------------------------------------------------------- layout -----
def story_elements(doc: Doc, spec: dict) -> None:
    key, title = spec["key"], spec["title"]
    status = spec["status"]
    fill, stroke = STATUS[status]
    is_retired = status == "RETIRED"
    is_ai = spec["theme"] == "ai"

    # ------------------------------------------------------------- header --
    doc.text("hdr_title", 60, 40, f"{key}  {title}", 34, T_TITLE)
    status_rect = doc.rect("status_rect", 2040, 40, 300, 56, fill, stroke, 2)
    doc.fit_text(status_rect, spec["status_text"], 15, stroke, 30, min_fs=13)
    doc.text("hdr_sub", 60, 94,
             f"{spec['module']}   |   feature flag: {spec['flag']}", 18, T_SUB)
    doc.text("hdr_why", 60, 124, f"Why: {spec['why']}", 18, T_DETAIL)
    needs = ", ".join(spec["needs"]) or "nothing"
    unblocks = ", ".join(spec["unblocks"]) or "not stated"
    doc.text("hdr_deps", 60, 154,
             f"Needs first: {needs}     ->     Unblocks: {unblocks}", 16,
             T_DETAIL)
    doc.line("hdr_div", 60, 192, [[0, 0], [2280, 0]], T_DETAIL, 1, True)

    # --------------------------------------------------------- left: ACE ---
    ace = spec["ace"]
    if ace:
        hub = doc.rect("ace_hub", 60, 220, 660, 72, ACE_FILL, ACE_STROKE)
        doc.fit_text(hub, "ACE database  ->  recovery.v_ace_* views "
                       "(read-only)", 18, ACE_STROKE, 59, min_fs=15)
    else:
        hub = doc.rect("ace_hub", 60, 220, 660, 72, ACE_OFF_FILL,
                       ACE_OFF_STROKE, 1, True)
        doc.fit_text(hub, "ACE database: not touched by this story", 18,
                       ACE_OFF_STROKE, 59, min_fs=15)
        doc.wrapped_text("ace_note", 102, 316, spec["ace_note"], 16, T_DETAIL,
                         60)

    last_dot_center = None
    has_b = False
    for i, item in enumerate(ace):
        row = 316 + i * 56
        section = item["section"]
        if section == "B":
            has_b = True
            dot_fill, dot_stroke = B_FILL, B_STROKE
            name_color = B_STROKE
        else:
            dot_fill, dot_stroke = ACE_FILL, ACE_STROKE
            name_color = T_TITLE
        doc.dot(f"ace_leaf{i}_dot", 78, row + 5, 12, dot_fill, dot_stroke)
        doc.text(f"ace_leaf{i}_name", 102, row,
                 f"{item['view']}  [{section}]", 17, name_color)
        if item["note"]:
            doc.text(f"ace_leaf{i}_note", 102, row + 24, item["note"], 14,
                     T_DETAIL)
        last_dot_center = row + 11

    if ace and last_dot_center is not None:
        doc.line("ace_trunk", 84, 292, [[0, 0], [0, last_dot_center - 292]],
                 ACE_STROKE, 2)

    if has_b:
        legend_y = 316 + (len(ace) - 1) * 56 + 60
        doc.wrapped_text(
            "ace_legend", 102, legend_y,
            "[B] = Section B view: created after RWB-ACE-001; the feature "
            "stays behind its flag until then", 14, B_STROKE, 70)

    ace_arrow_color = ACE_STROKE if ace else ACE_OFF_STROKE
    doc.arrow("ace_arrow", 720, 256, [[0, 0], [90, 0], [90, 344], [238, 344]],
              ace_arrow_color, 2, dashed=not ace)
    doc.text("ace_arrow_lbl", 818, 420, "SELECT\nonly" if ace else "no\nread",
             14, ace_arrow_color)

    # ------------------------------------------------------ centre: hero ---
    trig_box = doc.rect("trig_box", 900, 220, 600, 200, TRIG_FILL,
                        TRIG_STROKE, 2)
    doc.text("trig_head", 920, 232, "WHAT STARTS IT", 18, TRIG_STROKE)
    for i, (tag, value) in enumerate(spec["triggers"]):
        doc.text(f"trig{i}", 920, 266 + i * 36, f"{tag:<6}{value}", 16,
                 T_BODY)

    goal = ("(Retired) " if is_retired else "") + spec["goal"]
    hero = doc.ellipse("hero", 960, 500, 480, 200, HERO_FILL, HERO_STROKE, 3)
    doc.fit_text(hero, goal, 20, T_ON_DARK, 26, min_fs=16, max_lines=5)
    doc.arrow("trig_arrow", 1200, 422, [[0, 0], [0, 76]], TRIG_STROKE, 2,
              sb=trig_box, eb=hero)

    doc.line("fn_link", 1200, 702, [[0, 0], [0, 56]], FN_STROKE, 2)
    fn_fill, fn_stroke = (AI_FILL, AI_STROKE) if is_ai else (FN_FILL, FN_STROKE)
    fn_hub = doc.rect("fn_hub", 900, 760, 600, 60, fn_fill, fn_stroke)
    doc.fit_text(fn_hub, "WHAT IT BUILDS (functions)", 18, fn_stroke, 40,
                     min_fs=15)
    doc.line("fn_stub", 1200, 820, [[0, 0], [0, 26]], fn_stroke, 1)
    doc.line("fn_bus", 830, 846, [[0, 0], [740, 0]], fn_stroke, 1)

    for i, fn in enumerate(spec["functions"]):
        col, row_i = i % 2, i // 2
        dx, row = 830 + col * 380, 866 + row_i * 64
        doc.dot(f"fn{i}_dot", dx, row + 5, 10, fn_fill, fn_stroke)
        doc.text(f"fn{i}_name", dx + 20, row, fn["name"], 16, T_TITLE)
        doc.text(f"fn{i}_does", dx + 20, row + 22, fn["does"], 14, T_DETAIL)

    # ----------------------------------------------------- right: tables ---
    rec_hub = doc.rect("rec_hub", 1680, 220, 660, 72, REC_FILL, REC_STROKE)
    doc.fit_text(rec_hub, "recovery schema  (Workbench-owned tables)", 18,
                   REC_STROKE, 59, min_fs=15)

    writes, reads = spec["writes"], spec["reads"]
    start_head = "arrow" if reads else None
    end_head = "arrow" if writes else None
    doc.arrow("rec_arrow", 1442, 600,
              [[0, 0], [148, 0], [148, -344], [238, -344]], REC_STROKE, 2,
              start=start_head, end=end_head)
    lbl = ("writes\n+ reads" if writes and reads
           else "writes" if writes
           else "reads" if reads
           else "no\ntables")
    doc.text("rec_arrow_lbl", 1598, 420, lbl, 14, REC_STROKE)

    cy = 316
    last_dot_center = None
    if writes:
        doc.text("rec_w_head", 1720, cy, "WRITES", 15, REC_STROKE)
        cy += 26
        for i, item in enumerate(writes):
            doc.dot(f"rec_w{i}_dot", 1698, cy + 5, 12, REC_FILL, REC_STROKE)
            doc.text(f"rec_w{i}_name", 1720, cy, item["t"], 16, REC_STROKE)
            if item["note"]:
                doc.text(f"rec_w{i}_note", 1720, cy + 22, item["note"], 14,
                         T_DETAIL)
            last_dot_center = cy + 11
            cy += 52
    cy += 10
    if reads:
        doc.text("rec_r_head", 1720, cy, "READS", 15, T_DETAIL)
        cy += 26
        for i, item in enumerate(reads):
            doc.dot(f"rec_r{i}_dot", 1699, cy + 5, 10, "#ffffff", T_DETAIL)
            name = item["t"] + ("  - " + item["note"] if item["note"] else "")
            doc.text(f"rec_r{i}", 1720, cy, name, 15, T_BODY)
            last_dot_center = cy + 10
            cy += 32
    cy += 10
    if not writes and not reads:
        doc.text("rec_none", 1700, cy,
                 "No Workbench table touched (build or pipeline story)", 16,
                 T_DETAIL)
        cy += 26
    if spec["stores"]:
        doc.text("rec_s_head", 1720, cy, "ALSO TOUCHES", 15, T_DETAIL)
        cy += 26
        doc.wrapped_text("rec_stores", 1720, cy, spec["stores"], 14, T_DETAIL,
                         70)
        cy += math.ceil(len(greedy_wrap(spec["stores"], 70)) * 14 * 1.25)
    if last_dot_center is not None:
        doc.line("rec_trunk", 1704, 292,
                 [[0, 0], [0, last_dot_center - 292]], REC_STROKE, 2)

    # ------------------------------------------------------------ path -----
    doc.text("path_head", 60, 1070,
             "HOW IT CONNECTS  (main path, left to right)", 20, T_TITLE)
    chips = spec["path"]
    n = len(chips)
    w = (2280 - (n - 1) * 56) // n
    xs = [60 + i * (w + 56) for i in range(n)]
    shapes = []
    for i, chip in enumerate(chips):
        kind, text = chip["kind"], chip["text"]
        fill, stroke, dashed = path_style(kind)
        if kind in ("trigger", "out"):
            shape = doc.ellipse(f"path_chip{i}", xs[i], 1110, w, 96, fill,
                                stroke, 1, dashed)
            chars = int((w * 0.8 - 10) / 9)
        else:
            shape = doc.rect(f"path_chip{i}", xs[i], 1110, w, 96, fill,
                             stroke, 1, dashed)
            chars = int((w - 24) / 9)
        doc.fit_text(shape, text, 15, stroke, max(chars, 8), min_fs=11,
                     max_lines=3)
        shapes.append(shape)
    for i in range(n - 1):
        doc.arrow(f"path_arrow{i}", xs[i] + w + 2, 1158,
                  [[0, 0], [xs[i + 1] - 2 - (xs[i] + w + 2), 0]], HERO_STROKE,
                  2, sb=shapes[i], eb=shapes[i + 1])

    # ----------------------------------------------------------- bottom ----
    doc.text("rules_head", 60, 1260, "RULES IT MUST KEEP", 20, RULE_STROKE)
    for i, rule in enumerate(spec["rules"]):
        doc.dot(f"rule{i}", 64, 1305 + i * 30, 10, RULE_FILL, RULE_STROKE)
        doc.text(f"rule{i}_txt", 84, 1300 + i * 30, rule, 16, T_BODY)

    doc.text("risks_head", 60, 1430,
             "WHAT CAN GO WRONG  ->  WHAT HAPPENS", 20, RISK_STROKE)
    for i, risk in enumerate(spec["risks"]):
        doc.dot(f"risk{i}", 64, 1475 + i * 30, 10, RISK_FILL, RISK_STROKE)
        doc.text(f"risk{i}_txt", 84, 1470 + i * 30, risk, 16, T_BODY)

    card = doc.rect("ex_card", 1200, 1250, 1140, 330, EX_FILL, EX_FILL)
    doc.text("ex_head", 1224, 1266, "EXAMPLE  (from the acceptance criteria)",
             16, EX_HEAD)
    for i, line in enumerate(spec["example"]):
        doc.text(f"ex_line{i}", 1224, 1300 + i * 30, line, 15, EX_BODY)
    del card

    doc.text("foot_src", 60, 1600,
             f"Source: 04 User stories / Epic 1 Story Files v6 / "
             f"{spec['file_stem']} ... | ACE tiers: 15 ACE DB Alignment / "
             f"ACE Data Tier Map v1", 13, T_DETAIL)
    doc.text("foot_key", 60, 1622,
             "Colour key: orange = what starts it | light blue = ACE read path "
             "| yellow = Section B or rule | green = Workbench table | mid blue "
             "= function | purple = AI agent | red = failure | dashed = store "
             "or not touched", 13, T_DETAIL)


def path_style(kind: str) -> tuple[str, str, bool]:
    if kind == "trigger":
        return TRIG_FILL, TRIG_STROKE, False
    if kind == "function":
        return FN_FILL, FN_STROKE, False
    if kind == "ace":
        return ACE_FILL, ACE_STROKE, False
    if kind == "table":
        return REC_FILL, REC_STROKE, False
    if kind == "store":
        return STORE_FILL, STORE_STROKE, True
    if kind == "ai":
        return AI_FILL, AI_STROKE, False
    if kind == "check":
        return RULE_FILL, RULE_STROKE, False
    if kind == "out":
        return OUT_FILL, OUT_STROKE, False
    raise AssertionError(f"unknown path kind {kind}")


# ------------------------------------------------------------- checks -------
def check_spec(spec: dict) -> list[str]:
    key = spec.get("key", "?")
    bad: list[str] = []

    def fail(field: str, problem: str) -> None:
        bad.append(f"{key}.{field}: {problem}")

    def limit_text(field: str, value: str, maximum: int) -> None:
        if len(value) > maximum:
            fail(field, f"{len(value)} chars (limit {maximum}): {value!r}")

    limit_text("title", spec["title"], LIMITS["title"])
    limit_text("status_text", spec["status_text"], LIMITS["status_text"])
    limit_text("goal", spec["goal"], LIMITS["goal"])
    limit_text("why", spec["why"], LIMITS["why"])
    limit_text("stores", spec["stores"], LIMITS["stores"])
    limit_text("overview_label", spec["overview_label"],
               LIMITS["overview_label"])

    if spec["status"] not in STATUS:
        fail("status", f"unknown status {spec['status']!r}")
    if spec["theme"] not in THEMES:
        fail("theme", f"unknown theme {spec['theme']!r}")
    if spec["module"] not in MODULES:
        fail("module", f"unknown module {spec['module']!r}")

    if not 1 <= len(spec["triggers"]) <= LIMITS["triggers"]:
        fail("triggers", f"{len(spec['triggers'])} items (1-4)")
    for i, (tag, value) in enumerate(spec["triggers"]):
        if tag not in TRIGGER_TAGS:
            fail(f"triggers[{i}]", f"unknown tag {tag!r}")
        if len(tag + value) > 54:
            fail(f"triggers[{i}]", f"{len(tag + value)} chars: {tag} {value!r}")

    if len(spec["ace"]) > LIMITS["ace"]:
        fail("ace", f"{len(spec['ace'])} items (0-8)")
    for i, item in enumerate(spec["ace"]):
        if item["section"] not in ("A", "B"):
            fail(f"ace[{i}].section", f"unknown section {item['section']!r}")
        if len(f"{item['view']}  [{item['section']}]") > 34:
            fail(f"ace[{i}].view", f"too long: {item['view']!r}")
        limit_text(f"ace[{i}].note", item["note"], 70)
    if not spec["ace"]:
        limit_text("ace_note", spec["ace_note"], 180)
        if not spec["ace_note"]:
            fail("ace_note", "required when ace is empty")

    for list_name, maximum in (("writes", 5), ("reads", 5)):
        if len(spec[list_name]) > maximum:
            fail(list_name, f"{len(spec[list_name])} items (0-{maximum})")
    for i, item in enumerate(spec["writes"]):
        limit_text(f"writes[{i}].t", item["t"], 34)
        limit_text(f"writes[{i}].note", item["note"], 70)
    for i, item in enumerate(spec["reads"]):
        limit_text(f"reads[{i}]", item["t"] + "  - " + item["note"], 66)

    if not spec["stores"]:
        fail("stores", "must not be empty")

    if not 1 <= len(spec["functions"]) <= LIMITS["functions"]:
        fail("functions", f"{len(spec['functions'])} items (1-6)")
    for i, fn in enumerate(spec["functions"]):
        if len(fn["name"]) > NAME_LIMIT:
            fail(f"functions[{i}].name", f"too long: {fn['name']!r}")
        limit_text(f"functions[{i}].does", fn["does"], 40)

    if not 3 <= len(spec["path"]) <= 6:
        fail("path", f"{len(spec['path'])} chips (3-6)")
    for i, chip in enumerate(spec["path"]):
        if chip["kind"] not in PATH_KINDS:
            fail(f"path[{i}].kind", f"unknown kind {chip['kind']!r}")
        limit_text(f"path[{i}].text", chip["text"], 60)

    if not 1 <= len(spec["rules"]) <= LIMITS["rules"]:
        fail("rules", f"{len(spec['rules'])} items (1-4)")
    for i, rule in enumerate(spec["rules"]):
        limit_text(f"rules[{i}]", rule, 108)

    if not 1 <= len(spec["risks"]) <= LIMITS["risks"]:
        fail("risks", f"{len(spec['risks'])} items (1-3)")
    for i, risk in enumerate(spec["risks"]):
        limit_text(f"risks[{i}]", risk, 108)

    if not 1 <= len(spec["example"]) <= LIMITS["example"]:
        fail("example", f"{len(spec['example'])} lines (1-8)")
    for i, line in enumerate(spec["example"]):
        limit_text(f"example[{i}]", line, 118)

    for i, need in enumerate(spec["needs"] + spec["unblocks"]):
        if not NEED.match(need):
            fail("needs", f"bad key {need!r}")

    deps = ("Needs first: " + (", ".join(spec["needs"]) or "nothing") +
            "     ->     Unblocks: " +
            (", ".join(spec["unblocks"]) or "not stated"))
    if len(deps) > 230:
        fail("header", f"dependency line {len(deps)} chars (limit 230)")

    if len(greedy_wrap(spec["stores"], 70)) > 3:
        fail("stores", "wraps to more than 3 lines of 70")

    if spec["example"]:
        last = 1300 + (len(spec["example"]) - 1) * 30 + 19
        if last > 1580:
            fail("example", f"text ends at y{last}, card ends 1580")

    return bad


def check_elements(spec: dict, doc: Doc) -> list[str]:
    key = spec["key"]
    bad: list[str] = []
    els = doc.els

    # 2. inside the canvas ---------------------------------------------------
    for el in els:
        if el["type"] in ("line", "arrow"):
            xs = [el["x"] + p[0] for p in el["points"]]
            ys = [el["y"] + p[1] for p in el["points"]]
            x0, x1, y0, y1 = min(xs), max(xs), min(ys), max(ys)
        else:
            x0, x1 = el["x"], el["x"] + el["width"]
            y0, y1 = el["y"], el["y"] + el["height"]
        if x0 < 40 or x1 > 2360 or y0 < 20 or y1 > 1660:
            bad.append(f"{key}.element {el['id']}: outside the canvas "
                       f"({x0:.0f},{y0:.0f})-({x1:.0f},{y1:.0f})")

    # 3. overlap -------------------------------------------------------------
    free = [e for e in els if e["type"] == "text" and e["containerId"] is None]
    boxes = {e["id"]: (e["x"], e["y"], e["x"] + e["width"],
                       e["y"] + e["height"]) for e in free}
    for i, a in enumerate(free):
        for b in free[i + 1:]:
            if boxes_overlap(boxes[a["id"]], boxes[b["id"]]):
                bad.append(f"{key}.overlap text {a['id']} / {b['id']}")

    shapes = [e for e in els if e["type"] in ("rectangle", "ellipse")]
    containers = {e["id"]: boxes_text(e) for e in els
                  if e["id"] in ("trig_box", "ex_card")}
    for t in free:
        for s in shapes:
            if not boxes_overlap(boxes[t["id"]], bounds(s)):
                continue
            inside = any(box_contains(cb, boxes[t["id"]])
                         for cb in containers.values())
            if not inside:
                bad.append(f"{key}.overlap text {t['id']} / shape {s['id']}")

    # bound text must fit its container --------------------------------------
    for el in els:
        if el["type"] != "text" or el["containerId"] is None:
            continue
        parent = next(e for e in els if e["id"] == el["containerId"])
        if el["height"] > parent["height"] - 6:
            bad.append(f"{key}.fit {el['id']}: text height {el['height']} "
                       f"vs container {parent['height']}")
        if el["width"] > parent["width"] and el["textAlign"] != "center":
            bad.append(f"{key}.fit {el['id']}: text wider than container")

    # 4. references resolve --------------------------------------------------
    ids = {e["id"] for e in els}
    for el in els:
        for ref in el.get("boundElements") or []:
            if ref["id"] not in ids:
                bad.append(f"{key}.ref {el['id']}: boundElements -> "
                           f"{ref['id']} missing")
        for field in ("startBinding", "endBinding"):
            b = el.get(field)
            if b and b["elementId"] not in ids:
                bad.append(f"{key}.ref {el['id']}: {field} -> "
                           f"{b['elementId']} missing")
    for el in els:
        if el["type"] == "text" and el["containerId"] is not None:
            parent = next(e for e in els if e["id"] == el["containerId"])
            if el["id"] not in [r["id"] for r in parent["boundElements"]]:
                bad.append(f"{key}.ref {el['id']}: parent does not list it")
    return bad


def bounds(el: dict) -> tuple:
    if el["type"] in ("line", "arrow"):
        xs = [el["x"] + p[0] for p in el["points"]]
        ys = [el["y"] + p[1] for p in el["points"]]
        return min(xs), min(ys), max(xs), max(ys)
    return el["x"], el["y"], el["x"] + el["width"], el["y"] + el["height"]


def boxes_text(el: dict) -> tuple:
    return el["x"], el["y"], el["x"] + el["width"], el["y"] + el["height"]


def boxes_overlap(a: tuple, b: tuple, tol: int = 2) -> bool:
    ox = min(a[2], b[2]) - max(a[0], b[0])
    oy = min(a[3], b[3]) - max(a[1], b[1])
    return ox > tol and oy > tol


def box_contains(outer: tuple, inner: tuple) -> bool:
    return (inner[0] >= outer[0] and inner[1] >= outer[1]
            and inner[2] <= outer[2] and inner[3] <= outer[3])


NEED = re.compile(r"^(?:E1|E2|TE)-\d{3}$|^ACE-\d{3}$")


# ------------------------------------------------------------- modules ------
MODULES = {
    "P1 Recovery data engine": "P1",
    "P1 Recovery data engine (technical enabler)": "P1",
    "P2 Integration": "P2",
    "P2 Integration (technical enabler)": "P2",
    "P3 Case and workflow": "P3",
    "P3 Case and workflow (technical enabler)": "P3",
    "P4 Access and administration": "P4",
    "P5 Document hub": "P5",
    "P5 Document hub (technical enabler)": "P5",
    "P6 Communications": "P6",
    "P7 Decision center and log": "P7",
    "P7 Decision center and log (technical enabler)": "P7",
    "P9 Reporting": "P9",
    "P10 Agent runtime": "P10",
    "P10 Agent runtime (technical enabler)": "P10",
}


# ----------------------------------------------------------------- main -----
def build_story(spec: dict, index: int) -> dict:
    doc = Doc(index)
    story_elements(doc, spec)
    problems = check_spec(spec) + check_elements(spec, doc)
    return {"doc": doc, "problems": problems, "spec": spec}


def write_doc(doc: Doc, path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    data = {
        "type": "excalidraw",
        "version": 2,
        "source": "recovery-workbench-story-maps",
        "elements": doc.els,
        "appState": {"gridSize": None, "viewBackgroundColor": "#ffffff"},
        "files": {},
    }
    path.write_text(json.dumps(data, indent=2, ensure_ascii=True) + "\n",
                    encoding="utf-8")


def load_specs() -> list[dict]:
    specs = []
    for path in sorted(SPECS.glob("*.json")):
        specs.append(json.loads(path.read_text(encoding="utf-8")))
    specs.sort(key=lambda s: (0 if s["key"].startswith("RWB-E1") else 1,
                              s["key"]))
    return specs


def build_overview(specs: list[dict]) -> dict:
    """The Epic 1 at a glance map (section 5.4)."""
    doc = Doc(len(specs) + 1)
    doc.text("ov_title", 80, 40,
             "Epic 1 at a glance: 71 stories, one ACE read path, one recovery "
             "schema", 36, T_TITLE)
    doc.text("ov_sub", 80, 96,
             "[A] reads Section A ACE views  [B] needs a Section B view "
             "(RWB-ACE-001)  [R] retired. Open each story map for detail.",
             18, T_DETAIL)

    top = [("P1", "P1 Recovery data engine", 80, 700, 160),
           ("P3", "P3 Case and workflow", 860, 700, 160),
           ("P5", "P5 Document hub", 1640, 700, 160),
           ("P2", "P2 Integration", 2420, 700, 160)]
    bottom = [("P4", "P4 Access and administration", 80, 560, 1180),
              ("P6", "P6 Communications", 700, 560, 1180),
              ("P7", "P7 Decision center and log", 1320, 560, 1180),
              ("P9", "P9 Reporting", 1940, 560, 1180),
              ("P10", "P10 Agent runtime", 2560, 560, 1180)]

    groups: dict[str, list[dict]] = {}
    for spec in specs:
        groups.setdefault(MODULES[spec["module"]], []).append(spec)

    def draw_block(code: str, label: str, x: int, w: int, y: int) -> dict:
        is_ai = code == "P10"
        fill, stroke = (AI_FILL, AI_STROKE) if is_ai else (FN_FILL, FN_STROKE)
        head = doc.rect(f"ov_{code}_head", x, y, w, 64, fill, stroke)
        doc.bound_text(head, label, 18, stroke, int((w - 20) / 10.8))
        rows = sorted(groups.get(code, []), key=lambda s: s["key"])
        for j, spec in enumerate(rows):
            ry = y + 80 + j * 30
            tags = []
            if any(a["section"] == "A" for a in spec["ace"]):
                tags.append("[A]")
            if any(a["section"] == "B" for a in spec["ace"]):
                tags.append("[B]")
            if spec["status"] == "RETIRED":
                tags.append("[R]")
            short = spec["key"].replace("RWB-", "")
            text = f"{short}  {spec['overview_label']}"
            if tags:
                text += "  " + "".join(tags)
            color = "#b91c1c" if spec["status"] == "RETIRED" else T_BODY
            doc.dot(f"ov_{code}_dot{j}", x + 4, ry + 6, 10, fill, stroke)
            doc.text(f"ov_{code}_row{j}", x + 24, ry, text, 15, color)
        return head

    top_heads = [draw_block(*b) for b in top]
    bottom_heads = [draw_block(*b) for b in bottom]

    # middle band -----------------------------------------------------------
    ace = doc.rect("ov_ace", 80, 880, 440, 160, ACE_FILL, ACE_STROKE)
    doc.bound_text(ace, "ACE database (public.*)\none copy of all source data\n"
                        "loaded by ACE, never by the Workbench", 16,
                   ACE_STROKE, 40)
    views = doc.rect("ov_views", 640, 880, 440, 160, ACE_FILL, ACE_STROKE)
    doc.bound_text(views, "30 recovery.v_ace_* views\n16 Section A now (V0002)\n"
                          "14 Section B after RWB-ACE-001 (V0003)", 16,
                   ACE_STROKE, 40)
    hub = doc.ellipse("ov_hub", 1260, 840, 620, 240, HERO_FILL, HERO_STROKE, 3)
    doc.bound_text(hub, "Epic 1: Recovery Workbench foundation\n"
                        "71 story maps | release 30 Nov 2026", 20, T_ON_DARK, 40)
    backbone = doc.rect("ov_backbone", 2000, 860, 1140, 200, REC_FILL,
                        REC_STROKE)
    doc.bound_text(backbone,
                   "Shared backbone every story writes through:\n"
                   "decision_log_entry (E1-008, E1-027) | interaction ledger "
                   "(E1-066)\noutbox (TE-006) | Quartz jobs JOB-02..17 (TE-007) "
                   "| feature flags (E1-047)\ndocument containers (TE-012) | "
                   "parameters + reference data (E1-042, E1-043)", 16,
                   REC_STROKE, 74)

    doc.arrow("ov_a1", 520, 960, [[0, 0], [118, 0]], HERO_STROKE, 2,
              eb=views)
    doc.text("ov_a1_lbl", 530, 930, "ace_view_owner", 13, T_DETAIL)
    doc.arrow("ov_a2", 1080, 960, [[0, 0], [178, 0]], HERO_STROKE, 2,
              sb=views, eb=hub)
    doc.text("ov_a2_lbl", 1090, 930, "recovery_svc SELECT", 13, T_DETAIL)
    doc.arrow("ov_a3", 1882, 960, [[0, 0], [116, 0]], HERO_STROKE, 2,
              sb=hub, eb=backbone)

    # buses -----------------------------------------------------------------
    doc.line("ov_bus_top", 430, 800, [[0, 0], [2340, 0]], ACE_STROKE, 2)
    doc.line("ov_bus_top_stub", 1570, 800, [[0, 0], [0, 40]], ACE_STROKE, 2)
    for code, head in zip([b[0] for b in top], top_heads):
        rows = groups.get(code, [])
        last = head["y"] + 80 + (len(rows) - 1) * 30 + 19 + 8
        cx = head["x"] + head["width"] / 2
        doc.line(f"ov_stub_{code}", cx, 800, [[0, 0], [0, last - 800]],
                 ACE_STROKE, 2)

    doc.line("ov_bus_bottom", 360, 1130, [[0, 0], [2480, 0]], ACE_STROKE, 2)
    doc.line("ov_bus_bottom_stub", 1570, 1080, [[0, 0], [0, 50]],
             ACE_STROKE, 2)
    for code, head in zip([b[0] for b in bottom], bottom_heads):
        cx = head["x"] + head["width"] / 2
        doc.line(f"ov_stub_b_{code}", cx, 1130, [[0, 0], [0, 50]],
                 ACE_STROKE, 2)

    problems = check_overview(doc)
    return {"doc": doc, "problems": problems, "spec": {"key": "OVERVIEW"}}


def check_overview(doc: Doc) -> list[str]:
    """Bounds and free-text overlap for the overview (same rules)."""
    bad: list[str] = []
    free = [e for e in doc.els if e["type"] == "text"
            and e["containerId"] is None]
    for el in doc.els:
        x0, y0, x1, y1 = bounds(el)
        if x0 < 60 or x1 > 3160 or y0 < 20 or y1 > 1920:
            bad.append(f"OVERVIEW.element {el['id']}: outside the canvas "
                       f"({x0:.0f},{y0:.0f})-({x1:.0f},{y1:.0f})")
    for i, a in enumerate(free):
        for b in free[i + 1:]:
            if boxes_overlap(boxes_text(a), boxes_text(b)):
                bad.append(f"OVERVIEW.overlap text {a['id']} / {b['id']}")
    shapes = [e for e in doc.els if e["type"] in ("rectangle", "ellipse")]
    for t in free:
        for s in shapes:
            if boxes_overlap(boxes_text(t), bounds(s)):
                bad.append(f"OVERVIEW.overlap text {t['id']} / shape "
                           f"{s['id']}")
    return bad


def main(argv: list[str]) -> int:
    specs = load_specs()
    if not specs:
        print("no specs found")
        return 1
    wanted = argv[1:] if len(argv) > 1 else None
    problems: list[str] = []
    built = 0
    for index, spec in enumerate(specs, start=1):
        if wanted and spec["key"] not in wanted:
            continue
        result = build_story(spec, index)
        target = OUT / f"{spec['file_stem']}.excalidraw"
        if result["problems"]:
            problems.extend(result["problems"])
            print(f"FAIL {target.name}")
            for p in result["problems"]:
                print("  " + p)
        else:
            write_doc(result["doc"], target)
            built += 1
            print(f"OK {target.name}")
    if not wanted:
        overview = build_overview(specs)
        target = OUT / "00 Epic 1 at a glance.excalidraw"
        if overview["problems"]:
            problems.extend(overview["problems"])
            print(f"FAIL {target.name}")
            for p in overview["problems"]:
                print("  " + p)
        else:
            write_doc(overview["doc"], target)
            print(f"OK {target.name}")
            built += 1
    print(f"\n{built} file(s) written, {len(problems)} problem(s)")
    return 1 if problems else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
