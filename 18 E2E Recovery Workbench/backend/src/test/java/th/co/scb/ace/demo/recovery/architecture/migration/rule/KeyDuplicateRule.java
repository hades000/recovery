package th.co.scb.ace.demo.recovery.architecture.migration.rule;

import java.util.ArrayList;
import java.util.LinkedHashMap;
import java.util.List;
import java.util.Map;

import th.co.scb.ace.demo.recovery.architecture.migration.FolderContext;
import th.co.scb.ace.demo.recovery.architecture.migration.MigrationFinding;
import th.co.scb.ace.demo.recovery.architecture.migration.MigrationRule;
import th.co.scb.ace.demo.recovery.architecture.migration.ParsedMigrationFile;

/** SPEC-RWB-E1-044-006 (T-044-03, AC6): at most one non-fix file per story key. */
public final class KeyDuplicateRule implements MigrationRule {

	@Override
	public String ruleId() {
		return "L-KEY-DUP";
	}

	@Override
	public List<MigrationFinding> check(ParsedMigrationFile file, FolderContext folder) {
		return List.of();
	}

	@Override
	public List<MigrationFinding> checkFolder(FolderContext folder) {
		Map<String, String> firstByKey = new LinkedHashMap<>();
		List<MigrationFinding> findings = new ArrayList<>();
		for (ParsedMigrationFile file : folder.parsedFiles()) {
			if (!file.hasVersionedName() || file.isFix()) {
				continue;
			}
			String key = file.storyKey();
			String first = firstByKey.putIfAbsent(key, file.fileName());
			if (first != null) {
				findings.add(new MigrationFinding(ruleId(), file.fileName(), 0, key,
						"second non-fix file for story " + key + " (first: " + first + ")"));
			}
		}
		return findings;
	}

}
