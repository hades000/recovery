package th.co.scb.ace.demo.recovery.architecture.migration.rule;

import java.util.List;

import th.co.scb.ace.demo.recovery.architecture.migration.FolderContext;
import th.co.scb.ace.demo.recovery.architecture.migration.MigrationFinding;
import th.co.scb.ace.demo.recovery.architecture.migration.MigrationRule;
import th.co.scb.ace.demo.recovery.architecture.migration.ParsedMigrationFile;

/** SPEC-RWB-E1-044-006 (T-044-03): a fix file needs one non-fix file of its key below it. */
public final class FixNoBaseRule implements MigrationRule {

	@Override
	public String ruleId() {
		return "L-FIX-NO-BASE";
	}

	@Override
	public List<MigrationFinding> check(ParsedMigrationFile file, FolderContext folder) {
		if (!file.hasVersionedName() || !file.isFix()) {
			return List.of();
		}
		String key = file.storyKey();
		long baseFiles = folder.parsedFiles()
			.stream()
			.filter(candidate -> candidate.hasVersionedName() && !candidate.isFix())
			.filter(candidate -> key.equals(candidate.storyKey()) && candidate.sequence() < file.sequence())
			.count();
		if (baseFiles == 1) {
			return List.of();
		}
		return List.of(new MigrationFinding(ruleId(), file.fileName(), 0, key,
				"fix file needs one non-fix file of the same story with a lower sequence"));
	}

}
