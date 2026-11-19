# Epic 1 story maps - how they are built

One mind map per Epic 1 story file (60 E1 + 11 TE) plus `00 Epic 1 at a glance`,
each as an editable `.excalidraw` with a rendered `.png` beside it.

## Read one map

The centre ellipse is the story goal. The four branches answer four questions:

| Branch | Question | Colour |
|---|---|---|
| left | Where does the data come from? | light blue = `recovery.v_ace_*` view (amber = Section B, waits for RWB-ACE-001) |
| top | What starts the story? | orange |
| bottom | What does it build? | mid blue = function, purple = AI agent |
| right | What does it write and read? | green = `recovery.*` table |

The strip headed **HOW IT CONNECTS** is the same path as one line, left to right.
The dark card holds one real example from the acceptance criteria; the footer
repeats the colour key.

## Rebuild

```
python make_specs.py            # source/*.txt -> specs/*.json (enforces limits)
python build_story_maps.py      # all 71 maps + overview (prints OK per file)
python build_story_maps.py RWB-E1-069   # one story
python render_all.py            # .excalidraw -> .png
python verify.py                # counts, JSON references, 5 spot checks
```

`source/*.txt` holds the story blocks; `specs/*.json` is the generated input to
the layout engine. Edit the source, not the JSON, unless you are fixing a single
value.

## Checks the builder runs before writing a file

- every field limit from the plan (`title` 66, `goal` 110, `why` 180, ...);
- every element inside x 40-2360, y 20-1660;
- no free text overlaps another free text or a shape it does not belong to;
- every bound text fits its container, shrinking the font if needed;
- every `boundElements` and `containerId` reference resolves.

## Template notes

- `render/render_template.html` pins `@excalidraw/excalidraw@0.17.6`. The shared
  template's unpinned `?bundle` import now pulls a dependency that esm.sh serves
  as 404, so the module graph never loads. Nothing else in the renderer changed.
- The `WRITES` / `READS` / `ALSO TOUCHES` headings sit at x1720, aligned with the
  item text, so the green trunk line at x1704 does not run through them.
- Path chips size their text to the chip (font 15 down to 12, three lines max) so
  long endpoint names such as `/cases/{caseId}/documents` stay inside the shape.
- `functions[].name` allows 36 characters: the longest Flyway file name
  (`V0001__rwb_e1_001_recovery_schema`) is 35.
- When a story has no writes and no reads, the "No Workbench table touched" note
  comes first and `ALSO TOUCHES` follows it, so neither overlaps.
