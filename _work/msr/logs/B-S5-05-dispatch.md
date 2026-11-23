# B-S5-05 dispatch

Fanout 5, one subagent per legacy key: RWB-E4-030, RWB-E4-031, RWB-E4-032, RWB-E4-033, RWB-E4-034.
Each writes its own APP and CON story, its two fragments and its own gap and assumption part files.
The orchestrator merges the part files into gaps/B-S5-05.jsonl and assumptions/B-S5-05.jsonl, writes the edit log and runs the quick check.
