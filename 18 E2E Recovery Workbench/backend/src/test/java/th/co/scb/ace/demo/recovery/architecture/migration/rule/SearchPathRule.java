package th.co.scb.ace.demo.recovery.architecture.migration.rule;

import java.util.ArrayList;
import java.util.List;
import java.util.Locale;

import th.co.scb.ace.demo.recovery.architecture.migration.FolderContext;
import th.co.scb.ace.demo.recovery.architecture.migration.MigrationFinding;
import th.co.scb.ace.demo.recovery.architecture.migration.MigrationRule;
import th.co.scb.ace.demo.recovery.architecture.migration.ParsedMigrationFile;

/**
 * SPEC-RWB-E1-044-007 (T-044-20): any {@code search_path} identifier fails, in every form. The rule
 * runs on the code text, where strings are kept, so {@code set_config('search_path', …)} is caught.
 */
public final class SearchPathRule implements MigrationRule {

	@Override
	public String ruleId() {
		return "L-SEARCH-PATH";
	}

	@Override
	public List<MigrationFinding> check(ParsedMigrationFile file, FolderContext folder) {
		List<String> lines = file.codeText().lines().toList();
		List<MigrationFinding> findings = new ArrayList<>();
		for (int index = 0; index < lines.size(); index++) {
			if (lines.get(index).toLowerCase(Locale.ROOT).contains("search_path")) {
				findings.add(new MigrationFinding(ruleId(), file.fileName(), index + 1, null,
						"SET search_path is forbidden"));
			}
		}
		return findings;
	}

}
