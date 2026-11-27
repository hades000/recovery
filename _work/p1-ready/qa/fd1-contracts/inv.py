import yaml,glob,os,re,sys
M=('get','put','post','patch','delete')
for f in sorted(glob.glob('*.yaml')):
    if f=='index.yaml': continue
    d=yaml.safe_load(open(f,encoding='utf-8'))
    n=sum(1 for p in d['paths'].values() for m in p if m in M)
    xs=d.get('x-service',{})
    raw=open(f,'rb').read()
    pats=set(re.findall(rb'\^MSG-[^\'"\n]+',raw))
    jobs=[p for p in d['paths'] if 'job' in p]
    print(f,n,xs.get('operations'),d['info']['version'],'CRLF' if b'\r\n' in raw else 'LF',pats,jobs)
