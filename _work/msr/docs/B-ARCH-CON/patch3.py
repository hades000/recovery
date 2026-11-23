from pathlib import Path

p = Path("_work/msr/docs/B-ARCH-CON/build.py")
t = p.read_text(encoding="utf-8")
subs = [
    ('''                        "The provider's published contract and its fake" if pair_class(p, c) == "C" else "The edge stub named in section 8.4",''',
     '''                        {"C": "The provider's published contract and its fake",
                         "H": "Its own contract and its own contract test",
                         "X": "The edge stub named in section 8.4"}[pair_class(p, c)],'''),
    ('"The call-type matrix marks S5 to P6 as Temporal, but the write-off, asset, debt sale, litigation, guarantee and payment contracts name no communications interface for rwb-asset"',
     '"The call-type matrix marks S5 to P6 as Temporal, but the asset contract on Architecture v5 slide 19 names no communications interface and no other slide supplies one"'),
    ('L.append("Every pair in the matrix, resolved to the interface the sources name. The order is provider code, then consumer code, then call type. The dependency class is the class of Template and Rules \\u00a7R5.4 that the consuming story takes: C means the consuming story builds against the provider\'s published contract and its fake, and X means the pair crosses an edge outside the 19 services and is tracked, not built against.")',
     'L.append("Every pair in the matrix, resolved to the interface the sources name. The order is provider code, then consumer code, then call type. The dependency class is the class of Template and Rules \\u00a7R5.4 that the consuming story takes: C means the consuming story builds against the provider\'s published contract and its fake, X means the pair crosses an edge outside the 19 services and is tracked rather than built against, and H appears once, where rwb-case consumes its own CaseAllocationFailed.")'),
]
for a, b in subs:
    if a not in t:
        raise SystemExit("NOT FOUND: " + a[:90])
    t = t.replace(a, b)
p.write_text(t, encoding="utf-8")
print("patched", len(subs))
