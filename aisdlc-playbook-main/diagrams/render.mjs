#!/usr/bin/env node
// Renders a .drawio file (uncompressed XML) to an SVG with the diagram embedded and the shape
// hyperlinks kept, for use when the draw.io desktop app is not installed. Supports the subset of
// draw.io used by the playbook diagrams: rounded/plain rectangles, rhombus, ellipse, swimlanes
// (horizontal and vertical headers), text cells, HTML labels with <br> and <font color>, and
// straight or orthogonal edges with optional waypoints and exit/entry ports.
//
// Usage: node render.mjs <in.drawio> <out.svg>
import { readFileSync, writeFileSync } from 'node:fs';

const [, , input, output] = process.argv;
if (!input || !output) {
  console.error('Usage: node render.mjs <in.drawio> <out.svg>');
  process.exit(1);
}
const xml = readFileSync(input, 'utf8');

// ---------------------------------------------------------------- minimal XML parser
function parse(src) {
  const root = { name: '#root', attrs: {}, children: [] };
  const stack = [root];
  const re = /<\?[^>]*\?>|<!--[\s\S]*?-->|<(\/?)([\w:.-]+)((?:\s+[\w:.-]+\s*=\s*"[^"]*")*)\s*(\/?)>/g;
  let m;
  while ((m = re.exec(src))) {
    if (m[0].startsWith('<?') || m[0].startsWith('<!--')) continue;
    const [, close, name, attrText, selfClose] = m;
    if (close) { stack.pop(); continue; }
    const attrs = {};
    for (const a of attrText.matchAll(/([\w:.-]+)\s*=\s*"([^"]*)"/g)) attrs[a[1]] = decode(a[2]);
    const node = { name, attrs, children: [] };
    stack[stack.length - 1].children.push(node);
    if (!selfClose) stack.push(node);
  }
  return root;
}
function decode(s) {
  return s.replace(/&lt;/g, '<').replace(/&gt;/g, '>').replace(/&quot;/g, '"').replace(/&#39;/g, "'").replace(/&#(\d+);/g, (_, n) => String.fromCharCode(+n)).replace(/&nbsp;/g, '\u00a0').replace(/&amp;/g, '&');
}
const find = (node, name) => node.children.find((c) => c.name === name);
const findAll = (node, name) => node.children.filter((c) => c.name === name);

// ---------------------------------------------------------------- model
const doc = parse(xml);
const mxfile = find(doc, 'mxfile');
const diagram = find(mxfile, 'diagram');
const model = find(diagram, 'mxGraphModel');
const rootCell = find(model, 'root');
const pageW = +model.attrs.pageWidth || 1100;
const pageH = +model.attrs.pageHeight || 600;

const cells = new Map();
const order = [];
for (const node of rootCell.children) {
  let cell = node, label = node.attrs.value ?? '', link = null, id = node.attrs.id;
  if (node.name === 'UserObject' || node.name === 'object') {
    label = node.attrs.label ?? '';
    link = node.attrs.link ?? null;
    id = node.attrs.id;
    cell = find(node, 'mxCell');
  }
  if (!cell || cell.name !== 'mxCell') continue;
  const geo = find(cell, 'mxGeometry');
  const style = parseStyle(cell.attrs.style ?? '');
  const points = [];
  if (geo) {
    const arr = findAll(geo, 'Array').find((a) => a.attrs.as === 'points');
    if (arr) for (const p of findAll(arr, 'mxPoint')) points.push({ x: +p.attrs.x, y: +p.attrs.y });
  }
  const c = {
    id, label, link, style,
    vertex: cell.attrs.vertex === '1', edge: cell.attrs.edge === '1',
    parent: cell.attrs.parent, source: cell.attrs.source, target: cell.attrs.target,
    x: geo ? +(geo.attrs.x ?? 0) : 0, y: geo ? +(geo.attrs.y ?? 0) : 0,
    w: geo ? +(geo.attrs.width ?? 0) : 0, h: geo ? +(geo.attrs.height ?? 0) : 0,
    points,
  };
  cells.set(id, c);
  order.push(c);
}
function parseStyle(s) {
  const st = {};
  for (const part of s.split(';')) {
    if (!part) continue;
    const i = part.indexOf('=');
    if (i < 0) st[part] = true; else st[part.slice(0, i)] = part.slice(i + 1);
  }
  return st;
}
// absolute geometry
function abs(c) {
  if (c._abs) return c._abs;
  let x = c.x, y = c.y;
  const p = cells.get(c.parent);
  if (p && p.vertex) { const pa = abs(p); x += pa.x; y += pa.y; }
  return (c._abs = { x, y, w: c.w, h: c.h });
}

// ---------------------------------------------------------------- helpers
const escXml = (s) => String(s).replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;').replace(/"/g, '&quot;');
const FONT = 'Helvetica, Arial, sans-serif';
const charW = (fs) => fs * 0.54;

// Convert an HTML-ish label into lines of runs [{text, color, bold}]
function labelRuns(label) {
  const lines = [[]];
  let color = null;
  const tokens = label.split(/(<[^>]+>)/g);
  for (const t of tokens) {
    if (!t) continue;
    if (t.startsWith('<')) {
      const tag = t.toLowerCase();
      if (tag.startsWith('<br')) lines.push([]);
      else if (tag.startsWith('<font')) { const m = /color="([^"]+)"/i.exec(t); color = m ? m[1] : color; }
      else if (tag.startsWith('</font')) color = null;
      else if (tag.startsWith('<div') && lines[lines.length - 1].length) lines.push([]);
      continue;
    }
    lines[lines.length - 1].push({ text: decode(t), color });
  }
  return lines;
}
function wrapRuns(lines, maxChars) {
  const out = [];
  for (const runs of lines) {
    let cur = [], len = 0;
    const flush = () => { out.push(cur); cur = []; len = 0; };
    for (const r of runs) {
      for (const word of r.text.split(/(\s+)/).flatMap((w) => (w.length > maxChars ? w.split(/(?<=-)/) : [w]))) {
        if (!word) continue;
        if (/^\s+$/.test(word)) { if (len) { cur.push({ text: ' ', color: r.color }); len += 1; } continue; }
        if (len && len + word.length > maxChars) flush();
        if (word.length > maxChars) { // hard-break very long tokens such as paths
          let rest = word;
          while (rest.length > maxChars) { cur.push({ text: rest.slice(0, maxChars), color: r.color }); flush(); rest = rest.slice(maxChars); }
          cur.push({ text: rest, color: r.color }); len += rest.length; continue;
        }
        cur.push({ text: word, color: r.color }); len += word.length;
      }
    }
    out.push(cur);
  }
  return out.filter((l, i, a) => l.length || i < a.length - 1);
}
function textBlock({ label, x, y, w, h, fs, color, bold, italic, align = 'center', valign = 'middle', wrap = true, rotate = 0, padX = 4 }) {
  if (!label) return '';
  const maxChars = wrap ? Math.max(1, Math.floor((w - padX * 2) / charW(fs))) : 1e9;
  const lines = wrapRuns(labelRuns(label), maxChars);
  const lh = fs * 1.25;
  const total = lines.length * lh;
  let ty = valign === 'top' ? y + fs + 2 : valign === 'bottom' ? y + h - total + fs : y + (h - total) / 2 + fs * 0.9;
  const tx = align === 'left' ? x + padX : align === 'right' ? x + w - padX : x + w / 2;
  const anchor = align === 'left' ? 'start' : align === 'right' ? 'end' : 'middle';
  const parts = [];
  for (const runs of lines) {
    const spans = runs.map((r) => `<tspan${r.color ? ` fill="${r.color}"` : ''}>${escXml(r.text)}</tspan>`).join('');
    parts.push(`<text x="${tx.toFixed(1)}" y="${ty.toFixed(1)}" text-anchor="${anchor}" font-family="${FONT}" font-size="${fs}" fill="${color}"${bold ? ' font-weight="bold"' : ''}${italic ? ' font-style="italic"' : ''}>${spans}</text>`);
    ty += lh;
  }
  const g = parts.join('');
  return rotate ? `<g transform="rotate(${rotate} ${x + w / 2} ${y + h / 2})">${g}</g>` : g;
}

// ---------------------------------------------------------------- vertices
function renderVertex(c) {
  const st = c.style;
  const { x, y, w, h } = abs(c);
  const fill = st.fillColor && st.fillColor !== 'none' ? st.fillColor : 'none';
  const stroke = st.strokeColor && st.strokeColor !== 'none' ? st.strokeColor : 'none';
  const sw = st.strokeWidth ?? 1;
  const fs = +(st.fontSize ?? 12);
  const fc = st.fontColor ?? '#000000';
  const fstyle = +(st.fontStyle ?? 0);
  const bold = !!(fstyle & 1), italic = !!(fstyle & 2);
  const align = st.align ?? 'center';
  const valign = st.verticalAlign ?? 'middle';
  const dash = st.dashed === '1' ? ' stroke-dasharray="6 4"' : '';
  const r = st.rounded === '1' ? Math.min(8, h / 4) : 0;
  let shape = '', text = '';
  if (st.text !== undefined) {
    text = textBlock({ label: c.label, x, y, w, h, fs, color: fc, bold, italic, align, valign, wrap: st.whiteSpace === 'wrap' || c.label.includes('<br') });
  } else if (st.swimlane !== undefined) {
    const start = +(st.startSize ?? 30);
    const horizontal = st.horizontal !== '0';
    shape = `<rect x="${x}" y="${y}" width="${w}" height="${h}" rx="${r}" fill="#ffffff" stroke="${stroke}" stroke-width="${sw}"${dash}/>`;
    if (horizontal) {
      shape += `<rect x="${x}" y="${y}" width="${w}" height="${start}" rx="${r}" fill="${fill}" stroke="${stroke}" stroke-width="${sw}"/>` +
        `<line x1="${x}" y1="${y + start}" x2="${x + w}" y2="${y + start}" stroke="${stroke}" stroke-width="${sw}"/>`;
      text = textBlock({ label: c.label, x, y, w, h: start, fs, color: fc, bold: true, align: 'center' });
    } else {
      shape += `<rect x="${x}" y="${y}" width="${start}" height="${h}" rx="${r}" fill="${fill}" stroke="${stroke}" stroke-width="${sw}"/>` +
        `<line x1="${x + start}" y1="${y}" x2="${x + start}" y2="${y + h}" stroke="${stroke}" stroke-width="${sw}"/>`;
      // rotated header text: lay out in a box of width h and height start, then rotate -90
      const bx = x + start / 2 - h / 2, by = y + h / 2 - start / 2;
      text = textBlock({ label: c.label, x: bx, y: by, w: h, h: start, fs, color: fc, bold: true, align: 'center', rotate: -90, wrap: false });
    }
  } else if (st.rhombus !== undefined) {
    shape = `<polygon points="${x + w / 2},${y} ${x + w},${y + h / 2} ${x + w / 2},${y + h} ${x},${y + h / 2}" fill="${fill}" stroke="${stroke}" stroke-width="${sw}"${dash}/>`;
    text = textBlock({ label: c.label, x: x + w * 0.15, y, w: w * 0.7, h, fs, color: fc, bold, italic, align: 'center' });
  } else if (st.ellipse !== undefined) {
    shape = `<ellipse cx="${x + w / 2}" cy="${y + h / 2}" rx="${w / 2}" ry="${h / 2}" fill="${fill}" stroke="${stroke}" stroke-width="${sw}"${dash}/>`;
    text = textBlock({ label: c.label, x, y, w, h, fs, color: fc, bold, italic, align });
  } else {
    shape = `<rect x="${x}" y="${y}" width="${w}" height="${h}" rx="${r}" fill="${fill}" stroke="${stroke}" stroke-width="${sw}"${dash}/>`;
    const padX = +(st.spacingLeft ?? 4);
    text = textBlock({ label: c.label, x, y, w, h, fs, color: fc, bold, italic, align, valign, padX: Math.max(padX, 4) });
  }
  return wrapLink(c, `<g>${shape}${text}</g>`, c.label);
}
function wrapLink(c, inner, title) {
  if (!c.link) return inner;
  return `<a xlink:href="${escXml(c.link)}" href="${escXml(c.link)}" target="_top" style="cursor:pointer"><title>${escXml(stripTags(title))}</title>${inner}</a>`;
}
const stripTags = (s) => decode(s.replace(/<[^>]+>/g, ' ')).replace(/\s+/g, ' ').trim();

// ---------------------------------------------------------------- edges
function port(c, px, py) {
  const a = abs(c);
  return { x: a.x + a.w * px, y: a.y + a.h * py };
}
function perimeter(c, toward) {
  // intersection of the ray centre->toward with the cell's bounding box
  const a = abs(c);
  const cx = a.x + a.w / 2, cy = a.y + a.h / 2;
  const dx = toward.x - cx, dy = toward.y - cy;
  if (!dx && !dy) return { x: cx, y: cy };
  const sx = dx ? (a.w / 2) / Math.abs(dx) : Infinity;
  const sy = dy ? (a.h / 2) / Math.abs(dy) : Infinity;
  const s = Math.min(sx, sy);
  return { x: cx + dx * s, y: cy + dy * s };
}
function renderEdge(c) {
  const st = c.style;
  const s = cells.get(c.source), t = cells.get(c.target);
  if (!s || !t) return '';
  const stroke = st.strokeColor ?? '#000000';
  const sw = st.strokeWidth ?? 1;
  const dash = st.dashed === '1' ? ' stroke-dasharray="6 4"' : '';
  const ortho = st.edgeStyle === 'orthogonalEdgeStyle';
  const hasExit = st.exitX !== undefined, hasEntry = st.entryX !== undefined;
  let pts = [];
  const way = c.points;
  let p0 = hasExit ? port(s, +st.exitX, +st.exitY) : null;
  let p1 = hasEntry ? port(t, +st.entryX, +st.entryY) : null;
  if (!p0) p0 = perimeter(s, way[0] ?? p1 ?? centre(t));
  if (!p1) p1 = perimeter(t, way[way.length - 1] ?? p0);
  if (way.length) {
    pts = [p0, ...way, p1];
    if (ortho) pts = orthogonalise(pts);
  } else if (ortho) {
    const dx = p1.x - p0.x, dy = p1.y - p0.y;
    if (hasExit && (+st.exitY === 0 || +st.exitY === 1) && Math.abs(dx) > 1) {
      // leave vertically, then horizontal, then vertical into the target
      const midY = hasEntry && (+st.entryY === 0 || +st.entryY === 1) ? (p0.y + p1.y) / 2 : p1.y;
      pts = midY === p1.y ? [p0, { x: p0.x, y: p1.y }, p1] : [p0, { x: p0.x, y: midY }, { x: p1.x, y: midY }, p1];
    } else if (Math.abs(dx) >= Math.abs(dy)) {
      const midX = (p0.x + p1.x) / 2;
      pts = Math.abs(dy) < 1 ? [p0, p1] : [p0, { x: midX, y: p0.y }, { x: midX, y: p1.y }, p1];
    } else {
      const midY = (p0.y + p1.y) / 2;
      pts = Math.abs(dx) < 1 ? [p0, p1] : [p0, { x: p0.x, y: midY }, { x: p1.x, y: midY }, p1];
    }
  } else {
    pts = [p0, p1];
  }
  const d = pts.map((p, i) => `${i ? 'L' : 'M'}${p.x.toFixed(1)} ${p.y.toFixed(1)}`).join(' ');
  const marker = st.endArrow && st.endArrow !== 'none' ? ` marker-end="url(#arrow-${markerId(stroke)})"` : '';
  markers.set(markerId(stroke), stroke);
  let label = '';
  if (c.label) {
    const mid = midpoint(pts);
    const fs = +(st.fontSize ?? 11);
    const text = stripTags(c.label);
    const tw = text.length * charW(fs) + 8;
    label = `<rect x="${(mid.x - tw / 2).toFixed(1)}" y="${(mid.y - fs * 0.8).toFixed(1)}" width="${tw.toFixed(1)}" height="${fs * 1.5}" fill="#ffffff" opacity="0.9"/>` +
      `<text x="${mid.x.toFixed(1)}" y="${(mid.y + fs * 0.35).toFixed(1)}" text-anchor="middle" font-family="${FONT}" font-size="${fs}" fill="${st.fontColor ?? stroke}">${escXml(text)}</text>`;
  }
  return `<g><path d="${d}" fill="none" stroke="${stroke}" stroke-width="${sw}"${dash}${marker} stroke-linejoin="round"/>${label}</g>`;
}
function centre(c) { const a = abs(c); return { x: a.x + a.w / 2, y: a.y + a.h / 2 }; }
function orthogonalise(pts) {
  // insert elbows so each segment is axis-aligned, keeping the given waypoints
  const out = [pts[0]];
  for (let i = 1; i < pts.length; i++) {
    const a = out[out.length - 1], b = pts[i];
    if (Math.abs(a.x - b.x) > 0.5 && Math.abs(a.y - b.y) > 0.5) {
      const next = pts[i + 1];
      // choose the elbow that keeps the following segment axis-aligned when possible
      if (next && Math.abs(next.x - b.x) < 0.5) out.push({ x: a.x, y: b.y }); else out.push({ x: b.x, y: a.y });
    }
    out.push(b);
  }
  return out;
}
function midpoint(pts) {
  let total = 0; const segs = [];
  for (let i = 1; i < pts.length; i++) { const l = Math.hypot(pts[i].x - pts[i - 1].x, pts[i].y - pts[i - 1].y); segs.push(l); total += l; }
  let acc = 0;
  for (let i = 0; i < segs.length; i++) {
    if (acc + segs[i] >= total / 2) {
      const t = (total / 2 - acc) / (segs[i] || 1);
      return { x: pts[i].x + (pts[i + 1].x - pts[i].x) * t, y: pts[i].y + (pts[i + 1].y - pts[i].y) * t };
    }
    acc += segs[i];
  }
  return pts[0];
}
const markers = new Map();
const markerId = (color) => color.replace(/[^a-zA-Z0-9]/g, '');

// ---------------------------------------------------------------- render
const vertices = order.filter((c) => c.vertex && c.id !== '0' && c.id !== '1');
const edges = order.filter((c) => c.edge);
const bodyV = vertices.map(renderVertex).join('\n');
const bodyE = edges.map(renderEdge).join('\n');
// bounds
let maxX = 0, maxY = 0;
for (const c of vertices) { const a = abs(c); maxX = Math.max(maxX, a.x + a.w); maxY = Math.max(maxY, a.y + a.h); }
for (const c of edges) for (const p of c.points) { maxX = Math.max(maxX, p.x); maxY = Math.max(maxY, p.y); }
const W = Math.max(pageW, Math.ceil(maxX + 20)), H = Math.max(Math.min(pageH, Math.ceil(maxY + 20)), Math.ceil(maxY + 20));
const defs = `<defs>${[...markers].map(([id, color]) => `<marker id="arrow-${id}" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="8" markerHeight="8" orient="auto-start-reverse"><path d="M0 0 L10 5 L0 10 z" fill="${color}"/></marker>`).join('')}</defs>`;
const svg = `<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" version="1.1" width="${W}px" height="${H}px" viewBox="0 0 ${W} ${H}" content="${escXml(xml.trim())}">
<rect width="100%" height="100%" fill="#ffffff"/>
${defs}
${bodyV}
${bodyE}
</svg>
`;
writeFileSync(output, svg);
console.log(`rendered ${output} (${W}x${H}, ${vertices.length} shapes, ${edges.length} edges, ${vertices.filter((c) => c.link).length} links)`);
