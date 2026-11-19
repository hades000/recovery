package th.co.scb.ace.demo.recovery.architecture.migration.rule;

import java.util.ArrayList;
import java.util.List;

import th.co.scb.ace.demo.recovery.architecture.migration.FolderContext;
import th.co.scb.ace.demo.recovery.architecture.migration.MigrationFinding;
import th.co.scb.ace.demo.recovery.architecture.migration.MigrationRule;
import th.co.scb.ace.demo.recovery.architecture.migration.ParsedMigrationFile;

/** SPEC-RWB-E1-044-006 (T-044-03): a second {@code -- Story:} line anywhere in the file fails. */
public final class HeaderMultiRule implements MigrationRule {

	@Override
	public String ruleId() {
		return "L-HEADER-MULTI";
	}

	@Override
	public List<MigrationFinding> check(ParsedMigrationFile file, FolderContext folder) {
		List<MigrationFinding> findings = new ArrayList<>();
		List<String> lines = file.rawLines();
		for (int index = 1; index < lines.size(); index++) {
			if (lines.get(index).strip().startsWith("-- Story:")) {
				findings.add(new MigrationFinding(ruleId(), file.fileName(), index + 1, null, "second -- Story: line"));
			}
		}
		return findings;
	}

}
