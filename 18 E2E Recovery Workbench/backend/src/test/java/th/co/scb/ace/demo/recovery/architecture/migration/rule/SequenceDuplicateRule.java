package th.co.scb.ace.demo.recovery.architecture.migration.rule;

import java.util.ArrayList;
import java.util.LinkedHashMap;
import java.util.List;
import java.util.Map;

import th.co.scb.ace.demo.recovery.architecture.migration.FolderContext;
import th.co.scb.ace.demo.recovery.architecture.migration.MigrationFinding;
import th.co.scb.ace.demo.recovery.architecture.migration.MigrationRule;
import th.co.scb.ace.demo.recovery.architecture.migration.ParsedMigrationFile;

/** SPEC-RWB-E1-044-005 (T-044-01): two files with the same sequence are one finding naming both. */
public final class SequenceDuplicateRule implements MigrationRule {

	@Override
	public String ruleId() {
		return "L-SEQ-DUP";
	}

	@Override
	public List<MigrationFinding> check(ParsedMigrationFile file, FolderContext folder) {
		return List.of();
	}

	@Override
	public List<MigrationFinding> checkFolder(FolderContext folder) {
		Map<Integer, List<String>> bySequence = new LinkedHashMap<>();
		for (ParsedMigrationFile file : folder.parsedFiles()) {
			if (file.sequence() >= 0) {
				bySequence.computeIfAbsent(file.sequence(), sequence -> new ArrayList<>()).add(file.fileName());
			}
		}
		List<MigrationFinding> findings = new ArrayList<>();
		for (Map.Entry<Integer, List<String>> entry : bySequence.entrySet()) {
			List<String> files = entry.getValue();
			if (files.size() > 1) {
				String sequence = String.format("%04d", entry.getKey());
				findings.add(new MigrationFinding(ruleId(), files.get(files.size() - 1), 0, sequence,
						"duplicate sequence V" + sequence + " in " + String.join(" and ", files)));
			}
		}
		return findings;
	}

}
