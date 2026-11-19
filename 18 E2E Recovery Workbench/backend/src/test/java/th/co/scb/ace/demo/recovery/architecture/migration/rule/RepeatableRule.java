package th.co.scb.ace.demo.recovery.architecture.migration.rule;

import java.util.List;

import th.co.scb.ace.demo.recovery.architecture.migration.FolderContext;
import th.co.scb.ace.demo.recovery.architecture.migration.MigrationFinding;
import th.co.scb.ace.demo.recovery.architecture.migration.MigrationRule;
import th.co.scb.ace.demo.recovery.architecture.migration.ParsedMigrationFile;

/** SPEC-RWB-E1-044-005 (T-044-01): a repeatable {@code R__*.sql} file is refused. */
public final class RepeatableRule implements MigrationRule {

	@Override
	public String ruleId() {
		return "L-REPEATABLE";
	}

	@Override
	public List<MigrationFinding> check(ParsedMigrationFile file, FolderContext folder) {
		if (!ParsedMigrationFile.isRepeatableName(file.fileName())) {
			return List.of();
		}
		return List.of(new MigrationFinding(ruleId(), file.fileName(), 0, file.fileName(),
				"repeatable migrations are forbidden"));
	}

}
