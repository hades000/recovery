package th.co.scb.ace.demo.recovery.architecture.migration.rule;

import java.util.List;

import th.co.scb.ace.demo.recovery.architecture.migration.FolderContext;
import th.co.scb.ace.demo.recovery.architecture.migration.MigrationFinding;
import th.co.scb.ace.demo.recovery.architecture.migration.MigrationRule;
import th.co.scb.ace.demo.recovery.architecture.migration.ParsedMigrationFile;

/** SPEC-RWB-E1-044-006 (T-044-03): a fix line must give a reason. */
public final class FixLine2Rule implements MigrationRule {

	private static final String FIX = "-- Fix:";

	@Override
	public String ruleId() {
		return "L-FIX-LINE2";
	}

	@Override
	public List<MigrationFinding> check(ParsedMigrationFile file, FolderContext folder) {
		if (!file.hasVersionedName() || !file.isFix()) {
			return List.of();
		}
		String line = file.rawLines().get(1);
		String reason = line.substring(FIX.length()).strip();
		if (!reason.isEmpty()) {
			return List.of();
		}
		return List.of(new MigrationFinding(ruleId(), file.fileName(), 2, null,
				"fix line needs a reason after -- Fix:"));
	}

}
