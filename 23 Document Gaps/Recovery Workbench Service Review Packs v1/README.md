# Recovery Workbench Service Review Packs v1

Decision: D-RCV-60. Date: 26 November 2026. Status: Draft (directive resolutions). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

One folder per service. Run the reviewer prompt on one service at a time: give it the service's review pack, its resolved-items file and the staged story files listed in section 2 of the pack, together with the documents the stories cite. Fix the findings in the next version of the files, then move on.

Master records: Gap Register v2, Assumptions Register v2 and Cross-document Change Register v1 (23 Document Gaps).

| Service | Stories | Resolved | Cross-document | Not applied | Business decisions | Lint | Pack size |
|---|---|---|---|---|---|---|---|
| RWB-ITG-NFR Non-functional integration | 2 | 28 | 23 | 1 | 4 | 0 | 15 KB |
| RWB-ITG-W1 Wave 1 integration (part 1 of 5) | 7 | 203 | 240 | 4 | 23 | 2 | 129 KB |
| RWB-ITG-W1 Wave 1 integration (part 2 of 5) | 13 | 325 | 171 | 14 | 35 | 3 | 109 KB |
| RWB-ITG-W1 Wave 1 integration (part 3 of 5) | 10 | 158 | 165 | 8 | 31 | 0 | 101 KB |
| RWB-ITG-W1 Wave 1 integration (part 4 of 5) | 11 | 217 | 193 | 18 | 26 | 0 | 117 KB |
| RWB-ITG-W1 Wave 1 integration (part 5 of 5) | 11 | 183 | 218 | 21 | 15 | 0 | 105 KB |
| RWB-ITG-W2 Wave 2 integration (part 1 of 5) | 7 | 145 | 165 | 18 | 30 | 2 | 108 KB |
| RWB-ITG-W2 Wave 2 integration (part 2 of 5) | 8 | 179 | 175 | 21 | 44 | 4 | 123 KB |
| RWB-ITG-W2 Wave 2 integration (part 3 of 5) | 8 | 147 | 160 | 19 | 27 | 2 | 109 KB |
| RWB-ITG-W2 Wave 2 integration (part 4 of 5) | 11 | 166 | 191 | 27 | 28 | 1 | 123 KB |
| RWB-ITG-W2 Wave 2 integration (part 5 of 5) | 9 | 158 | 139 | 19 | 11 | 4 | 76 KB |
| RWB-ITG-W3 Wave 3 integration | 9 | 176 | 134 | 2 | 11 | 4 | 59 KB |
| RWB-ITG-W4 Wave 4 integration (part 1 of 2) | 19 | 325 | 213 | 27 | 14 | 1 | 94 KB |
| RWB-ITG-W4 Wave 4 integration (part 2 of 2) | 22 | 382 | 191 | 20 | 24 | 1 | 103 KB |
| RWB-PLT-DB ACE DB schemas and logins | 2 | 22 | 25 | 11 | 0 | 0 | 15 KB |
| RWB-PLT-EDGE Edge and gateway (part 1 of 2) | 1 | 12 | 186 | 1 | 8 | 0 | 122 KB |
| RWB-PLT-EDGE Edge and gateway (part 2 of 2) | 4 | 41 | 177 | 20 | 8 | 0 | 123 KB |
| RWB-PLT-EVT Kafka event platform | 3 | 21 | 19 | 7 | 0 | 1 | 12 KB |
| RWB-PLT-LIB Shared libraries (part 1 of 4) | 3 | 49 | 203 | 17 | 22 | 0 | 130 KB |
| RWB-PLT-LIB Shared libraries (part 2 of 4) | 5 | 69 | 173 | 9 | 16 | 0 | 86 KB |
| RWB-PLT-LIB Shared libraries (part 3 of 4) | 9 | 154 | 231 | 17 | 18 | 2 | 115 KB |
| RWB-PLT-LIB Shared libraries (part 4 of 4) | 1 | 26 | 92 | 3 | 5 | 0 | 54 KB |
| RWB-PLT-OBS Observability | 2 | 28 | 33 | 7 | 0 | 0 | 13 KB |
| RWB-PLT-TPL Service template and repositories | 19 | 177 | 293 | 29 | 16 | 2 | 113 KB |
| RWB-PLT-WF Temporal workflow platform | 16 | 161 | 377 | 11 | 9 | 1 | 123 KB |
| RWB-SVC-P1 rwb-source-data (Source data) (part 1 of 7) | 17 | 319 | 227 | 13 | 23 | 0 | 91 KB |
| RWB-SVC-P1 rwb-source-data (Source data) (part 2 of 7) | 9 | 184 | 255 | 12 | 14 | 1 | 105 KB |
| RWB-SVC-P1 rwb-source-data (Source data) (part 3 of 7) | 9 | 180 | 231 | 6 | 21 | 4 | 107 KB |
| RWB-SVC-P1 rwb-source-data (Source data) (part 4 of 7) | 10 | 200 | 209 | 18 | 14 | 2 | 93 KB |
| RWB-SVC-P1 rwb-source-data (Source data) (part 5 of 7) | 9 | 152 | 208 | 9 | 22 | 3 | 94 KB |
| RWB-SVC-P1 rwb-source-data (Source data) (part 6 of 7) | 7 | 153 | 240 | 1 | 37 | 0 | 119 KB |
| RWB-SVC-P1 rwb-source-data (Source data) (part 7 of 7) | 1 | 20 | 22 | 4 | 4 | 0 | 20 KB |
| RWB-SVC-P10 rwb-agent (Agent) (part 1 of 3) | 14 | 273 | 262 | 10 | 19 | 0 | 94 KB |
| RWB-SVC-P10 rwb-agent (Agent) (part 2 of 3) | 11 | 225 | 226 | 15 | 12 | 0 | 84 KB |
| RWB-SVC-P10 rwb-agent (Agent) (part 3 of 3) | 15 | 239 | 251 | 14 | 17 | 1 | 88 KB |
| RWB-SVC-P2 rwb-integration (Integration) (part 1 of 4) | 6 | 169 | 246 | 4 | 18 | 0 | 102 KB |
| RWB-SVC-P2 rwb-integration (Integration) (part 2 of 4) | 7 | 100 | 205 | 7 | 24 | 0 | 94 KB |
| RWB-SVC-P2 rwb-integration (Integration) (part 3 of 4) | 8 | 161 | 247 | 7 | 25 | 4 | 98 KB |
| RWB-SVC-P2 rwb-integration (Integration) (part 4 of 4) | 6 | 94 | 161 | 10 | 12 | 0 | 64 KB |
| RWB-SVC-P3 rwb-case (Case and workflow) (part 1 of 12) | 7 | 184 | 248 | 7 | 20 | 1 | 117 KB |
| RWB-SVC-P3 rwb-case (Case and workflow) (part 2 of 12) | 9 | 206 | 210 | 4 | 18 | 0 | 91 KB |
| RWB-SVC-P3 rwb-case (Case and workflow) (part 3 of 12) | 11 | 173 | 190 | 9 | 22 | 2 | 80 KB |
| RWB-SVC-P3 rwb-case (Case and workflow) (part 4 of 12) | 6 | 106 | 158 | 3 | 13 | 0 | 91 KB |
| RWB-SVC-P3 rwb-case (Case and workflow) (part 5 of 12) | 5 | 122 | 214 | 4 | 17 | 1 | 114 KB |
| RWB-SVC-P3 rwb-case (Case and workflow) (part 6 of 12) | 7 | 131 | 201 | 22 | 25 | 1 | 101 KB |
| RWB-SVC-P3 rwb-case (Case and workflow) (part 7 of 12) | 6 | 116 | 220 | 24 | 29 | 2 | 108 KB |
| RWB-SVC-P3 rwb-case (Case and workflow) (part 8 of 12) | 8 | 183 | 179 | 28 | 30 | 2 | 99 KB |
| RWB-SVC-P3 rwb-case (Case and workflow) (part 9 of 12) | 7 | 122 | 170 | 27 | 32 | 1 | 97 KB |
| RWB-SVC-P3 rwb-case (Case and workflow) (part 10 of 12) | 8 | 166 | 171 | 45 | 28 | 11 | 110 KB |
| RWB-SVC-P3 rwb-case (Case and workflow) (part 11 of 12) | 7 | 78 | 244 | 30 | 6 | 1 | 93 KB |
| RWB-SVC-P3 rwb-case (Case and workflow) (part 12 of 12) | 3 | 49 | 47 | 18 | 10 | 0 | 36 KB |
| RWB-SVC-P4 rwb-access (Access and authority) (part 1 of 11) | 16 | 305 | 224 | 24 | 23 | 0 | 91 KB |
| RWB-SVC-P4 rwb-access (Access and authority) (part 2 of 11) | 15 | 272 | 216 | 27 | 11 | 1 | 90 KB |
| RWB-SVC-P4 rwb-access (Access and authority) (part 3 of 11) | 8 | 183 | 248 | 11 | 24 | 3 | 125 KB |
| RWB-SVC-P4 rwb-access (Access and authority) (part 4 of 11) | 8 | 176 | 151 | 25 | 28 | 0 | 91 KB |
| RWB-SVC-P4 rwb-access (Access and authority) (part 5 of 11) | 6 | 131 | 185 | 19 | 28 | 2 | 105 KB |
| RWB-SVC-P4 rwb-access (Access and authority) (part 6 of 11) | 8 | 150 | 192 | 31 | 30 | 2 | 115 KB |
| RWB-SVC-P4 rwb-access (Access and authority) (part 7 of 11) | 6 | 119 | 198 | 22 | 35 | 0 | 122 KB |
| RWB-SVC-P4 rwb-access (Access and authority) (part 8 of 11) | 8 | 144 | 192 | 21 | 35 | 0 | 108 KB |
| RWB-SVC-P4 rwb-access (Access and authority) (part 9 of 11) | 11 | 214 | 230 | 21 | 29 | 3 | 119 KB |
| RWB-SVC-P4 rwb-access (Access and authority) (part 10 of 11) | 22 | 342 | 244 | 13 | 18 | 0 | 85 KB |
| RWB-SVC-P4 rwb-access (Access and authority) (part 11 of 11) | 3 | 61 | 45 | 2 | 4 | 0 | 18 KB |
| RWB-SVC-P5 rwb-document (Document) (part 1 of 6) | 8 | 175 | 158 | 12 | 36 | 2 | 101 KB |
| RWB-SVC-P5 rwb-document (Document) (part 2 of 6) | 9 | 196 | 198 | 24 | 21 | 1 | 94 KB |
| RWB-SVC-P5 rwb-document (Document) (part 3 of 6) | 9 | 158 | 154 | 29 | 23 | 0 | 77 KB |
| RWB-SVC-P5 rwb-document (Document) (part 4 of 6) | 9 | 155 | 212 | 16 | 33 | 1 | 101 KB |
| RWB-SVC-P5 rwb-document (Document) (part 5 of 6) | 9 | 163 | 188 | 16 | 40 | 0 | 100 KB |
| RWB-SVC-P5 rwb-document (Document) (part 6 of 6) | 8 | 161 | 165 | 16 | 21 | 0 | 81 KB |
| RWB-SVC-P6 rwb-comms (Communications) (part 1 of 6) | 8 | 160 | 215 | 20 | 24 | 2 | 113 KB |
| RWB-SVC-P6 rwb-comms (Communications) (part 2 of 6) | 8 | 194 | 208 | 21 | 15 | 5 | 95 KB |
| RWB-SVC-P6 rwb-comms (Communications) (part 3 of 6) | 7 | 140 | 199 | 20 | 29 | 2 | 111 KB |
| RWB-SVC-P6 rwb-comms (Communications) (part 4 of 6) | 6 | 136 | 169 | 29 | 17 | 2 | 82 KB |
| RWB-SVC-P6 rwb-comms (Communications) (part 5 of 6) | 15 | 323 | 242 | 28 | 26 | 4 | 106 KB |
| RWB-SVC-P6 rwb-comms (Communications) (part 6 of 6) | 4 | 60 | 56 | 11 | 14 | 0 | 37 KB |
| RWB-SVC-P7 rwb-decision (Decision and rules) (part 1 of 8) | 6 | 113 | 174 | 31 | 19 | 1 | 89 KB |
| RWB-SVC-P7 rwb-decision (Decision and rules) (part 2 of 8) | 10 | 204 | 212 | 36 | 33 | 5 | 122 KB |
| RWB-SVC-P7 rwb-decision (Decision and rules) (part 3 of 8) | 7 | 129 | 206 | 24 | 35 | 0 | 123 KB |
| RWB-SVC-P7 rwb-decision (Decision and rules) (part 4 of 8) | 7 | 161 | 206 | 24 | 33 | 2 | 117 KB |
| RWB-SVC-P7 rwb-decision (Decision and rules) (part 5 of 8) | 6 | 99 | 158 | 25 | 24 | 0 | 92 KB |
| RWB-SVC-P7 rwb-decision (Decision and rules) (part 6 of 8) | 6 | 140 | 162 | 32 | 36 | 1 | 114 KB |
| RWB-SVC-P7 rwb-decision (Decision and rules) (part 7 of 8) | 9 | 178 | 201 | 40 | 28 | 0 | 119 KB |
| RWB-SVC-P7 rwb-decision (Decision and rules) (part 8 of 8) | 1 | 28 | 22 | 5 | 2 | 0 | 15 KB |
| RWB-SVC-P8 rwb-payment (Payment) (part 1 of 3) | 5 | 142 | 213 | 14 | 12 | 2 | 92 KB |
| RWB-SVC-P8 rwb-payment (Payment) (part 2 of 3) | 11 | 304 | 274 | 32 | 9 | 2 | 104 KB |
| RWB-SVC-P8 rwb-payment (Payment) (part 3 of 3) | 5 | 107 | 86 | 5 | 5 | 0 | 32 KB |
| RWB-SVC-P9 rwb-reporting (Reporting) | 12 | 222 | 253 | 43 | 11 | 3 | 98 KB |
| RWB-SVC-S1 rwb-valuation (Valuation and route) | 24 | 614 | 375 | 18 | 50 | 10 | 123 KB |
| RWB-SVC-S2 rwb-treatment (Treatment and offer) (part 1 of 4) | 6 | 113 | 213 | 12 | 26 | 3 | 115 KB |
| RWB-SVC-S2 rwb-treatment (Treatment and offer) (part 2 of 4) | 10 | 225 | 220 | 24 | 21 | 2 | 110 KB |
| RWB-SVC-S2 rwb-treatment (Treatment and offer) (part 3 of 4) | 20 | 395 | 257 | 23 | 20 | 0 | 82 KB |
| RWB-SVC-S2 rwb-treatment (Treatment and offer) (part 4 of 4) | 11 | 177 | 141 | 16 | 10 | 3 | 51 KB |
| RWB-SVC-S3 rwb-guarantee (Guarantee) | 17 | 364 | 208 | 18 | 27 | 2 | 82 KB |
| RWB-SVC-S4 rwb-litigation (Litigation) (part 1 of 3) | 14 | 295 | 229 | 10 | 30 | 2 | 96 KB |
| RWB-SVC-S4 rwb-litigation (Litigation) (part 2 of 3) | 18 | 375 | 238 | 15 | 51 | 13 | 91 KB |
| RWB-SVC-S4 rwb-litigation (Litigation) (part 3 of 3) | 13 | 265 | 201 | 10 | 19 | 7 | 70 KB |
| RWB-SVC-S5 rwb-asset (Asset) (part 1 of 4) | 13 | 278 | 262 | 20 | 31 | 0 | 98 KB |
| RWB-SVC-S5 rwb-asset (Asset) (part 2 of 4) | 18 | 398 | 248 | 36 | 29 | 1 | 88 KB |
| RWB-SVC-S5 rwb-asset (Asset) (part 3 of 4) | 17 | 429 | 242 | 20 | 24 | 17 | 88 KB |
| RWB-SVC-S5 rwb-asset (Asset) (part 4 of 4) | 3 | 75 | 69 | 0 | 3 | 0 | 24 KB |
| RWB-SVC-S6 rwb-debtsale (Debt sale) (part 1 of 3) | 14 | 342 | 253 | 17 | 34 | 1 | 90 KB |
| RWB-SVC-S6 rwb-debtsale (Debt sale) (part 2 of 3) | 15 | 293 | 265 | 5 | 74 | 0 | 98 KB |
| RWB-SVC-S6 rwb-debtsale (Debt sale) (part 3 of 3) | 1 | 20 | 15 | 0 | 3 | 0 | 7 KB |
| RWB-SVC-S7 rwb-writeoff (Write-off) (part 1 of 2) | 16 | 303 | 237 | 30 | 28 | 8 | 86 KB |
| RWB-SVC-S7 rwb-writeoff (Write-off) (part 2 of 2) | 16 | 321 | 210 | 22 | 29 | 5 | 83 KB |
| RWB-SVC-S8 rwb-deviation (Deviation) (part 1 of 3) | 9 | 248 | 196 | 18 | 38 | 6 | 117 KB |
| RWB-SVC-S8 rwb-deviation (Deviation) (part 2 of 3) | 16 | 397 | 212 | 24 | 21 | 0 | 85 KB |
| RWB-SVC-S8 rwb-deviation (Deviation) (part 3 of 3) | 6 | 117 | 74 | 8 | 11 | 0 | 33 KB |
| RWB-SVC-S9 rwb-partner (Partner) (part 1 of 3) | 15 | 304 | 232 | 21 | 12 | 11 | 108 KB |
| RWB-SVC-S9 rwb-partner (Partner) (part 2 of 3) | 17 | 343 | 251 | 20 | 17 | 2 | 89 KB |
| RWB-SVC-S9 rwb-partner (Partner) (part 3 of 3) | 4 | 87 | 50 | 5 | 6 | 0 | 20 KB |
| Programme-wide (no story) | 0 | 0 | 136 | 0 | 247 | 0 | 211 KB |

A service with a large pack is split into parts by story; review the parts one prompt at a time.
