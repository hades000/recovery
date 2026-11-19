package th.co.scb.ace.demo.recovery.architecture.migration.rule;

import java.util.List;

import th.co.scb.ace.demo.recovery.architecture.migration.FolderContext;
import th.co.scb.ace.demo.recovery.architecture.migration.MigrationFinding;
import th.co.scb.ace.demo.recovery.architecture.migration.MigrationRule;
import th.co.scb.ace.demo.recovery.architecture.migration.ParsedMigrationFile;

/** SPEC-RWB-E1-044-005 (T-044-04, AC7): an undo file is refused by its own rule ID. */
public final class UndoRule implements MigrationRule {

	@Override
	public String ruleId() {
		return "L-UNDO";
	}

	@Override
	public List<MigrationFinding> check(ParsedMigrationFile file, FolderContext folder) {
		if (!ParsedMigrationFile.isUndoName(file.fileName())) {
			return List.of();
		}
		return List.of(new MigrationFinding(ruleId(), file.fileName(), 0, file.fileName(),
				"undo migrations are forbidden"));
	}

}
