import sys,os,re,csv,shutil,time
exec(open(os.path.join(os.path.dirname(os.path.abspath(sys.argv[0])),'comp.py'),encoding='utf-8').read())
P=W+'/tc-backfill.csv'
rows=list(csv.reader(open(P,encoding='utf-8-sig')))
keep=[rows[0]]; seen=set(); drop=[]
for r in rows[1:]:
    k,a,t=r
    ok=(k,a,t) not in seen and t in tcs and tcs[t][12]=='Live'
    if ok and (k,a) in trace: ok=t in [x.strip() for x in str(trace[(k,a)][3]).split(',')]
    seen.add((k,a,t))
    (keep if ok else drop).append(r)
print('keep',len(keep)-1,'drop',len(drop))
if '--write' in sys.argv and drop:
    shutil.copy(P,os.path.join(os.path.dirname(os.path.abspath(sys.argv[0])),'tc-backfill-%s.bak'%time.strftime('%H%M%S')))
    with open(P,'w',encoding='utf-8',newline='') as f: csv.writer(f,quoting=csv.QUOTE_ALL).writerows(keep)
    L=W+'/editlog/W2-tests.csv'; csv.field_size_limit(10**9)
    n=max(int(m.group(1)) for r in csv.reader(open(L,encoding='utf-8-sig')) for m in [re.match(r'W2-tests-(\d+)$',r[0] if r else '')] if m)
    with open(L,'a',encoding='utf-8',newline='') as f:
        csv.writer(f,quoting=csv.QUOTE_ALL).writerow(['W2-tests-%04d'%(n+1),'REMOVE','tc-backfill.csv','','','superseded story, criterion, test case pairs',('; '.join('%s %s %s'%tuple(r) for r in drop))[:399]+'…','%d pairs removed (test case retired or re-pointed); %d pairs remain'%(len(drop),len(keep)-1),'','','','claude-sonnet-5-5','W2-tests'])
