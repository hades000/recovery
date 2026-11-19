import zipfile, shutil, os, re, tempfile

def load(path):
    z = zipfile.ZipFile(path)
    return z, z.read('word/document.xml').decode('utf-8'), z.read('docProps/core.xml').decode('utf-8')

def rep1(x, old, new, start=None):
    """Replace exactly one occurrence; if start given, the first occurrence after that anchor (anchor must be unique)."""
    if start is None:
        n = x.count(old)
        assert n == 1, (old, n)
        return x.replace(old, new)
    assert x.count(start) == 1, (start, x.count(start))
    a = x.index(start)
    i = x.index(old, a)
    return x[:i] + new + x[i + len(old):]

def set_modified(core, stamp='2026-11-15T09:00:00Z'):
    return re.sub(r'(<dcterms:modified[^>]*>)[^<]*(</dcterms:modified>)', r'\g<1>' + stamp + r'\g<2>', core)

def save(path, z, doc, core):
    fd, tmp = tempfile.mkstemp(suffix='.docx', dir=os.path.dirname(path)); os.close(fd)
    with zipfile.ZipFile(tmp, 'w') as out:
        for info in z.infolist():
            data = z.read(info.filename)
            if info.filename == 'word/document.xml': data = doc.encode('utf-8')
            elif info.filename == 'docProps/core.xml': data = core.encode('utf-8')
            out.writestr(info, data, compress_type=zipfile.ZIP_DEFLATED)
    z.close()
    shutil.move(tmp, path)
