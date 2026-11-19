import sys, zipfile, re
z = zipfile.ZipFile(sys.argv[1])
names = sorted([n for n in z.namelist() if re.match(r'ppt/slides/slide\d+\.xml$', n)], key=lambda n:int(re.findall(r'\d+',n)[0]))
only = sys.argv[2:] 
for n in names:
    if only and n not in only: continue
    x = z.read(n).decode('utf-8')
    print("=====", n, len(x))
    for sp in re.findall(r'<p:(?:sp|graphicFrame)>.*?</p:(?:sp|graphicFrame)>', x, re.S):
        nm = re.search(r'<p:cNvPr id="(\d+)" name="([^"]*)"', sp)
        paras = re.findall(r'<a:p>.*?</a:p>|<a:p/>', sp, re.S)
        out=[]
        for p in paras:
            ts = re.findall(r'<a:t>(.*?)</a:t>', p, re.S)
            if ts: out.append(ts)
        if out: print(f"[{nm.group(1)} {nm.group(2)}]", out)
others = [n for n in z.namelist() if 'notes' in n or 'docProps' in n]
print(others)
