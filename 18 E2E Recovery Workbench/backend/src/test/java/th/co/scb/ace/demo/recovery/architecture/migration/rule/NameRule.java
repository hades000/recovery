package th.co.scb.ace.demo.recovery.architecture.migration.rule;

import java.util.ArrayList;
import java.util.List;

import th.co.scb.ace.demo.recovery.architecture.migration.FolderContext;
import th.co.scb.ace.demo.recovery.architecture.migration.MigrationFinding;
import th.co.scb.ace.demo.recovery.architecture.migration.MigrationRule;
import th.co.scb.ace.demo.recovery.architecture.migration.ParsedMigrationFile;

/**
 * SPEC-RWB-E1-044-005 (T-044-01): the file name is {@code V<seq>__<story>_<name>.sql}. Undo and
 * repeatable files have their own rule, and every non-{@code .sql} entry except {@code README.md}
 * is reported here (ASM-E044-05).
 */
public final class NameRule implements MigrationRule {

	@Override
	public String ruleId() {
		return "L-NAME";
	}

	@Override
	public List<MigrationFinding> check(ParsedMigrationFile file, FolderContext folder) {
		if (ParsedMigrationFile.isUndoName(file.fileName()) || ParsedMigrationFile.isRepeatableName(file.fileName())
				|| file.hasVersionedName()) {
			return List.of();
		}
		return List.of(new MigrationFinding(ruleId(), file.fileName(), 0, file.fileName(),
				"name must be V<seq>__<story>_<name>.sql"));
	}

	@Override
	public List<MigrationFinding> checkFolder(FolderContext folder) {
		List<MigrationFinding> findings = new ArrayList<>();
		for (String name : folder.otherEntries()) {
			if ("README.md".equals(name)) {
				continue;
			}
			findings.add(new MigrationFinding(ruleId(), name, 0, name,
					"only .sql migration files and README.md belong here"));
		}
		return findings;
	}

}
