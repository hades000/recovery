"""Build the P1 hub from the previous hub and the current staged text."""
import base64
import gzip
import json
import re
from pathlib import Path

WORK = Path(__file__).resolve().parents[1]
SET = WORK.parents[1]
STAGE = WORK / 'stage'
LOG = SET / '24 P1 Developer Readiness v1'
HUB = 'Recovery Workbench Project Hub v{}.html'
PAYLOAD = re.compile(r'(<script type="application/octet-stream" id="payload">)([^<]+)(</script>)')
STORY = re.compile(r'^# (RWB-[A-Z0-9-]+) (.+)$')
ID_KIND = {'RWB': 'RWB', 'RD-P1': 'RD-P1', 'TC-P1': 'TC', 'GAP': 'GAP', 'ASM': 'ASM'}
EXTRA_IDS = r'RD-P1-\\d{3}|TC-P1-[A-Z0-9]+-[A-Z]{2,3}-\\d{2,3}'


def sections(data):
    lines = data.splitlines()
    if lines and STORY.fullmatch(lines[0]):
        return [{'h': lines[0][2:], 'l': 1, 't': '\n'.join(lines[1:]).strip()}]
    result = []
    heading, level, body, fenced = 'Top', 1, [], False
    for line in lines:
        if line.lstrip().startswith(('~~~', chr(96) * 3)):
            fenced = not fenced
        match = None if fenced else re.match(r'^(#{1,6})\s+(.+)$', line)
        if match:
            if body or heading != 'Top':
                result.append({'h': heading, 'l': level, 't': '\n'.join(body).strip()})
            heading, level, body = match[2], len(match[1]), []
        else:
            body.append(line)
    result.append({'h': heading, 'l': level, 't': '\n'.join(body).strip()})
    return result


def main():
    source = (SET / '14 Story Updates' / HUB.format(18)).read_text(encoding='utf-8')
    payload = PAYLOAD.search(source)
    model = json.loads(gzip.decompress(base64.b64decode(payload[2])))
    shell = source[:payload.start()] + source[payload.end():]
    expr = re.search(r"const IDRX=new RegExp\('([^']+)'", shell)[1]
    augmented = expr.replace('(', '(' + EXTRA_IDS + '|', 1)
    matcher = re.compile(augmented.replace('\\\\', '\\'))
    paths = [(p, STAGE) for p in STAGE.rglob('*.md')]
    for filename in ('rwb-case.yaml', 'rwb-source-data.yaml'):
        paths += [(p, STAGE) for p in STAGE.rglob(filename)]
    register = sorted(LOG.glob('Recovery Workbench P1 Decision Register v*.md'))[-1:]
    paths += [(p, SET) for p in register + sorted(LOG.glob('*P1*Readiness*.md'))]

    staged_keys = {}
    for p, root in sorted(paths):
        content = p.read_text(encoding='utf-8-sig')
        secs = sections(content)
        folder = p.relative_to(root).parts[0]
        doc_index = len(model['docs'])
        story = STORY.fullmatch(content.splitlines()[0]) if content else None
        if story:
            assert story[1] not in staged_keys, story[1]
            staged_keys[story[1]] = doc_index
        model['docs'].append({'folder': folder, 'file': p.name, 'ext': p.suffix[1:],
                              'name': p.stem, 'inzip': '', 'secs': secs,
                              'p1Stage': True, 'path': p.relative_to(root).as_posix()})
        for section_index, section in enumerate(secs):
            location = [doc_index, section_index]
            ids = set(matcher.findall(section['h'] + '\n' + section['t']))
            for identifier in sorted(ids):
                kind = next((v for k,v in ID_KIND.items() if identifier.startswith(k+'-')),
                            identifier.split('-')[0])
                ref = model['ids'].setdefault(identifier, {'k':kind,'u':[]})
                ref['u'].append(location)
                if story and identifier == story[1] or section['h'].startswith(identifier + ' '):
                    ref['d'] = location
                    ref['t'] = section['h']
    p1_count = sum(k.startswith('RWB-P1-') for k in staged_keys)
    assert p1_count == 62, p1_count
    for k in staged_keys:
        assert model['ids'][k]['d'] == [staged_keys[k], 0], k

    def replace(old, new):
        nonlocal source
        assert shell.count(old) == 1, old
        source = source.replace(old, new, 1)

    replace('Recovery Workbench project hub v18', 'Recovery Workbench project hub v19')
    replace('>v18</span> D-RCV-60: 19-service realignment',
            '>v19</span> D-RCV-60: P1 developer readiness (RD-P1 register)')
    replace(expr, augmented)
    replace('STORIES=STORIES.filter(s=>seen[s.k]?false:(seen[s.k]=1));',
            'STORIES.sort((a,b)=>Number(!!M.docs[b.d].p1Stage)-Number(!!M.docs[a.d].p1Stage));\n'
            '  STORIES=STORIES.filter(s=>seen[s.k]?false:(seen[s.k]=1));')
    replace('const i=M.docs.findIndex(d=>!d.inzip&&d.name.indexOf(n)>=0);',
            'const i=M.docs.findLastIndex(d=>!d.inzip&&d.name.indexOf(n)>=0);')
    encoded = base64.b64encode(gzip.compress(json.dumps(model,ensure_ascii=False,
               separators=(',', ':')).encode('utf-8'),mtime=0)).decode('ascii')
    source = PAYLOAD.sub(lambda m: m[1]+encoded+m[3], source,count=1)
    check = json.loads(gzip.decompress(base64.b64decode(PAYLOAD.search(source)[2])))
    assert check == model
    dest = STAGE / '14 Story Updates' / HUB.format(19)
    dest.parent.mkdir(exist_ok=True)
    temp = dest.with_suffix('.tmp')
    temp.write_text(source,encoding='utf-8',newline='')
    temp.replace(dest)
    print(f'{dest}: {p1_count} P1 stories, {len(staged_keys)} staged stories, {len(paths)} staged text documents')


if __name__ == '__main__':
    main()

