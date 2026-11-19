import re, sys, collections
lines = open(sys.argv[1], encoding="utf-8").read().splitlines()[:6130]
pat = re.compile(r"(?i)(?<![\w$])(recovery|ace|public)\.[a-z_]")
hits = [(i+1, l) for i, l in enumerate(lines) if not l.strip().startswith("--") and pat.search(l)]
print("non-comment lines matching lint literal-schema regex (lines 1-6130):", len(hits))
c = collections.Counter(l.split(" ")[2] if l.startswith("INSERT") else l[:30] for _, l in hits)
print(c.most_common(10))
schem = collections.Counter(m.group(1).lower() for _, l in hits for m in pat.finditer(l))
print(schem)
for i, l in hits[:3]: print(i, l[:200])
