from pathlib import Path

p = Path(r"_work/msr/docs/B-DELIVDOC-47/build_v3.py")
lines = p.read_text(encoding="utf-8").splitlines()
want = {
    257: "    header_pt=10.0, body_pt=11.0))",   # slide 7
    360: "                     header_pt=10.0, body_pt=11.0))",  # 10-13
    387: "    header_pt=10.0, body_pt=10.5))",   # 14
    414: "    header_pt=10.0, body_pt=10.5))",   # 15
    433: "    header_pt=10.0, body_pt=11.0))",   # 16
    450: "    header_pt=10.0, body_pt=11.0))",   # 17
    471: "    header_pt=10.0, body_pt=11.0))",   # 18
    487: "    header_pt=10.0, body_pt=11.0))",   # 19
}
for i, new in want.items():
    print(i, repr(lines[i - 1]), "->", repr(new))
    lines[i - 1] = new
p.write_text("\n".join(lines) + "\n", encoding="utf-8")
