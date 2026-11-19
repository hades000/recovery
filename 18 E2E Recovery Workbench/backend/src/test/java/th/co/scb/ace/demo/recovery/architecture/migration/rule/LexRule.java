package th.co.scb.ace.demo.recovery.architecture.migration.rule;

import java.util.ArrayList;
import java.util.List;

import th.co.scb.ace.demo.recovery.architecture.migration.FolderContext;
import th.co.scb.ace.demo.recovery.architecture.migration.LexProblem;
import th.co.scb.ace.demo.recovery.architecture.migration.MigrationFinding;
import th.co.scb.ace.demo.recovery.architecture.migration.MigrationRule;
import th.co.scb.ace.demo.recovery.architecture.migration.ParsedMigrationFile;

/** SPEC-RWB-E1-044-007, -004 (T-044-22): one finding per unterminated opener, on its line. */
public final class LexRule implements MigrationRule {

	@Override
	public String ruleId() {
		return "L-LEX";
	}

	@Override
	public List<MigrationFinding> check(ParsedMigrationFile file, FolderContext folder) {
		List<MigrationFinding> findings = new ArrayList<>();
		for (LexProblem problem : file.unterminated()) {
			findings.add(new MigrationFinding(ruleId(), file.fileName(), problem.line(),
					String.valueOf(problem.offset()), "unterminated " + problem.kind()));
		}
		return findings;
	}

}
