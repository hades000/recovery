# Edit log D2-HUB — Recovery Workbench Project Hub next version

Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash
Decision: D-RCV-60 microservice realignment. Date: 22 November 2026.

Sources read: `12 Project communication/Recovery Workbench Project Hub v14.html` (decoded: the index payload of 192 documents, 8726 codes, 157 embedded files and its single application script), `_work/msr/editlog/` (the 822 new files listed by every work package of the run), `Recovery Workbench Microservice Story Template and Rules v1.md` (§R1, §R3, §R5, §R8, §R9), `_work/msr/plan/ownership.json` and `Recovery Workbench Microservice Ownership Map v1.xlsx` (Services, Tables, Endpoints, Events, Workflows and activities, Jobs, Parameters, Rulings), `Recovery Workbench Architecture v5 Text Extract v1.md`, `Recovery Workbench Temporal and Drools Design Text Extract v1.md`, `_work/msr/plan/split_plan.json` (stats and legacy), `_work/msr/plan/ids.json`, and the folder listings of the twelve document folders for the current version of each document.
Nothing read was edited.

## Files written

- `12 Project communication/Recovery Workbench Project Hub v15.html`
- `_work/msr/gaps/D2-HUB.jsonl`
- `_work/msr/assumptions/D2-HUB.jsonl`
- `_work/msr/editlog/D2-HUB.md`
- Scratch: `_work/msr/docs/D2-HUB/build.py` (the rebuild), `verify.py`, `stats.py`, `unmapped.py`, `check12.py`, `smoke.js`, `smoke2.js` (headless render tests), `extract_js.py`, `dumpb64.py`, `collect.py`, `analyse.py`, and the data files `setfiles.json`, `newer.json`, `sizes.json`.

No file outside the WP "Write only" list was created or edited, and no existing file was edited: v14 is untouched and v15 is new.

## What was produced

The hub is one self-contained file. It was rebuilt from the v14 source, not from a blank page, so every section, ID, number and date of the source is kept character for character.

| Item | v14 | v15 |
|---|---|---|
| Documents in the index | 192 | 192 (unchanged text) |
| Codes in the index | 8726 | 8726 (unchanged) |
| Story pages | 332 | 332 (unchanged) |
| Embedded original files | 157 | 157 (unchanged) |
| Documents that name a Set v15 file | 0 | 151 |
| New files listed in the Set v15 tab | 0 | 822 |
| Folders in the Set v15 tab | 0 | 40 |
| Tabs | 8 | 9 (Set v15 added) |

### What changed, and only this

1. **Header.** The two §R8.1 lines are the first band of the page, above the search bar: "SCB Collections and Recovery. Henka Group, 22 November 2026." and "(C) Siam Commercial Bank and Henka Pte Ltd" (ASM-D2-HUB-5). The band, the brand, the browser title, the home page, the tab and the new tab all carry the label **Document set v15**. The sticky header grew by 30 px, so the main grid and the mobile side panel move from 86 px to 116 px.
2. **Change log.** The home page and the Set v15 tab carry the row `v15, 22 November 2026, D-RCV-60 microservice realignment, T3 Code / OpenCode / DeepSeek v4.1 Flash`. The source hub carried no change-log row, so none was removed.
3. **Links to the new files.** Each of the 151 documents that has a successor names it: on the card in the folder view ("Set v15: <file>"), on the document page ("Document set v15: <folder>/<file>") and as a button "See that folder in Set v15" that opens the new tab on that folder. The successor is the highest version of the same document family in the same folder on disk, the same extension preferred; no name is constructed.
4. **The Set v15 tab.** New tab listing all 822 files the run wrote, by folder, each row carrying the file name and the work package that wrote it (the edit log). The side panel groups them by folder with a count. The tab states that the Documents tab holds the text as embedded at the previous version.
5. **Epic plan.** One added sentence: every release date is tentative and is copied unchanged from the source documents (rule 10; ASM-D2-HUB-7).
6. **Home page.** A short section "What this version is" naming the 19 services, the reissued documents and the service story files, and pointing to the Set v15 tab.

### What was deliberately not changed

- The text of all 192 documents, the 8726 codes and the 332 story pages. The realignment is carried by links and the label, because re-extracting 822 files is a corpus conversion that this work package was not given (CG-D2-HUB-3; ASM-D2-HUB-3).
- The embedded original files. The download buttons still return the file that was embedded at v14, and the document page says which file replaces it.
- The Decisions tab, the Terms tab, the Codes tab, the search and the story renderer, other than the small patches above.

## Mapping rules used for the links

- Family = the file name without its ` v<n>` suffix, compared inside the same folder. A zip member (for example `… v4.zip / … v2.md`) is compared inside its folder, and the extracted folder of the newer zip is found by the recursive scan: FSD P3 v2 maps to `03 Requirements and specifications/Recovery Workbench Functional Specifications by Module v7/Recovery Workbench FSD P3 Case and workflow v5.md`.
- A successor must have a higher version than the embedded file. A higher version wins; between two at the same version, the same extension wins.
- 41 documents have no successor on disk and therefore show no Set v15 line. They are the process, screen, AI and delivery documents that this stage did not reissue (for example the Screen Specifications, the Business Rules HTML, the Training and Change Plan).
- Two families continue as a folder and not as one file (API Specification v5, Physical Schema v7). Their document pages name none; the Set v15 tab lists their files (CG-D2-HUB-1; ASM-D2-HUB-1).
- Five folder-12 deliverables of this stage were reissued while the hub was being built (Document Index to v14, Document Control Sheet to v13, Team Start Pack to v3.pptx, Executive Presentation CTO to v4.pptx, Project Overview to v5.pptx); the hub links to the highest version on disk at build time, so a reissue after the build needs a rebuild (CG-D2-HUB-2; ASM-D2-HUB-2).

## Counts

- Gap rows: 4 candidate rows in `_work/msr/gaps/D2-HUB.jsonl` (CG-D2-HUB-1 to -4). Numbered GAP-nnnn in step D1.
- Assumption rows: 7 candidate rows in `_work/msr/assumptions/D2-HUB.jsonl` (ASM-D2-HUB-1 to -7). Numbered ASM-nnnn in step D1.
- Placeholders in the document: none. The §R9 placeholder string is not used in the hub, because the hub quotes the source and its own metadata comes from the file system and the edit logs, not from a missing value.

## Checks

`python -I "22 Microservice Realignment/checks/run_all.py" --wp D2-HUB --quick` — C02, C03, C05, C12, C13 and C18 all PASS; the report is under `22 Microservice Realignment/checks/reports/wp-D2-HUB-*.md`.

Beyond the checker:

- The payload round-trips: it decompresses and parses to 192 documents, 8726 codes and 822 new-file rows.
- The application script passes `node --check`.
- A headless render test (stubbed DOM, real payload) boots the hub and renders every tab, every side panel, a folder view, a document page, a story group and both views of the Set v15 tab without an error.

## Notes

- The file is 27.6 MB, the same order as v14 (27.6 MB), because the 157 embedded files are copied byte for byte and only the index payload is recompressed.
- No person name, email address or issue-tracker reference was added. The hub keeps only what the source hub already held.
- No release date was changed or raised as a gap; the epic plan now says in words that the dates are tentative.
- No tracker call was made, no git commit, and no file outside the write list was touched.
- The Ownership Map gives a service for every resource but no row for a document, so the Set v15 tab names the work package that wrote each file and invents no owner (CG-D2-HUB-4; ASM-D2-HUB-4).
