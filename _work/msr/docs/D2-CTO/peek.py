import re, sys
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
p = sys.argv[1]
t = open(p, encoding="utf-8").read()
a = int(sys.argv[2]) if len(sys.argv) > 2 else 0
b = int(sys.argv[3]) if len(sys.argv) > 3 else 3000
if len(sys.argv) > 4:
    for m in re.finditer(sys.argv[4], t):
        print(t[max(0, m.start() - 400):m.start() + 700].replace("\n", " "))
        print("-----")
else:
    print(t[a:b])
