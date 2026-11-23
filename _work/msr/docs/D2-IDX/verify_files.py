import io, re, os

ROOT = os.getcwd()
names = set()
for dirpath, dirnames, filenames in os.walk(ROOT):
    dirnames[:] = [d for d in dirnames if d not in ('.git', '_work')]
    for f in filenames:
        names.add(f)
    for d in dirnames:
        names.add(d)

t = io.open('12 Project communication/Recovery Workbench Document Index v14.md', encoding='utf-8').read()
missing = set()
for m in re.finditer(r'Recovery Workbench ([^,;|]+?\.(?:md|docx|pptx|xlsx|sql|html|yaml|zip|csv|svg|excalidraw))', t):
    fn = 'Recovery Workbench ' + m.group(1).strip()
    if fn not in names:
        missing.add(fn)
print('missing files named:', sorted(missing))
