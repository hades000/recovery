import glob,re,io
for f in sorted(glob.glob('*APP*.md'))+sorted(glob.glob('*CON*.md')):
    for i,l in enumerate(open(f,encoding='utf-8'),1):
        if re.search(r'404',l) and re.search(r'\bflag|rwb\.(p1|dataengine|source-data)\.',l,re.I):
            m=re.search(r'.{0,150}404.{0,150}',l)
            print(f.split(' v3')[0][:26],i,m.group(0)[:300])
