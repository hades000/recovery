package th.co.scb.ace.demo.recovery.architecture.migration.rule;

import java.util.List;

import th.co.scb.ace.demo.recovery.architecture.migration.FolderContext;
import th.co.scb.ace.demo.recovery.architecture.migration.MigrationFinding;
import th.co.scb.ace.demo.recovery.architecture.migration.MigrationRule;
import th.co.scb.ace.demo.recovery.architecture.migration.ParsedMigrationFile;

/** SPEC-RWB-E1-044-006 (T-044-03): line 1 is exactly {@code -- Story: <KEY>}. */
public final class HeaderRule implements MigrationRule {

	@Override
	public String ruleId() {
		return "L-HEADER";
	}

	@Override
	public List<MigrationFinding> check(ParsedMigrationFile file, FolderContext folder) {
		if (!file.hasVersionedName()) {
			return List.of();
		}
		String expected = "-- Story: " + file.storyKey();
		if (!file.rawLines().isEmpty() && file.rawLines().get(0).strip().equals(expected)) {
			return List.of();
		}
		return List.of(new MigrationFinding(ruleId(), file.fileName(), 1, null, "line 1 must be '" + expected + "'"));
	}

}
