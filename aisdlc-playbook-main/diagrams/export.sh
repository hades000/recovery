#!/bin/sh
# Export every diagrams/*.drawio to static/diagrams/*.svg with the diagram embedded (so the SVG stays
# editable in draw.io) and the shape hyperlinks kept, then copy the .drawio source next to it.
#
# Uses the draw.io desktop app when installed (https://github.com/jgraph/drawio-desktop/releases);
# otherwise falls back to the bundled renderer (render.mjs), which covers the shapes used here.
# Usage: npm run diagrams   (from the playbook folder)
set -e
here=$(cd "$(dirname "$0")" && pwd)
out="$here/../static/diagrams"
mkdir -p "$out"
app=""
for c in "/Applications/draw.io.app/Contents/MacOS/draw.io" "$(command -v drawio || true)" "$(command -v draw.io || true)"; do
  [ -n "$c" ] && [ -x "$c" ] && app="$c" && break
done
for f in "$here"/*.drawio; do
  name=$(basename "$f" .drawio)
  if [ -n "$app" ]; then
    "$app" -x -f svg --embed-diagram -o "$out/$name.svg" "$f" >/dev/null 2>&1
    # draw.io turns absolute paths into file:/// links and opens them in a new tab; make them site paths
    # that open in the page (the SVG is embedded with <object>, so the frame must be the top window).
    sed -i.bak -e 's#href="file:///#href="/#g' -e 's/target="_blank"/target="_top"/g' \
        -e 's#<a xlink:href="/#<a target="_top" xlink:href="/#g' "$out/$name.svg" && rm -f "$out/$name.svg.bak"
    echo "exported $name.svg (draw.io)"
  else
    node "$here/render.mjs" "$f" "$out/$name.svg"
  fi
  cp "$f" "$out/$name.drawio"
done
[ -n "$app" ] || echo "note: draw.io desktop not found; used the bundled renderer"
