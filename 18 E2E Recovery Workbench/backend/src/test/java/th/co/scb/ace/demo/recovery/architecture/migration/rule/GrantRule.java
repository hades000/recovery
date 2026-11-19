package th.co.scb.ace.demo.recovery.architecture.migration.rule;

import java.util.ArrayList;
import java.util.List;
import java.util.TreeSet;
import java.util.regex.Pattern;

import th.co.scb.ace.demo.recovery.architecture.migration.FolderContext;
import th.co.scb.ace.demo.recovery.architecture.migration.MigrationFinding;
import th.co.scb.ace.demo.recovery.architecture.migration.MigrationRule;
import th.co.scb.ace.demo.recovery.architecture.migration.MigrationStatement;
import th.co.scb.ace.demo.recovery.architecture.migration.ParsedMigrationFile;

/**
 * SPEC-RWB-E1-044-009 (T-044-20): grants belong to the view story. The rule fails when GRANT or
 * REVOKE is the first word of a line (inherited) or of a statement (new, so {@code SELECT 1; GRANT
 * …} on one line is caught). The statement's first word is read from the identifier view (c), so a
 * leading comment never hides or supplies it; the line check runs on the code text, so
 * {@code -- GRANT …} and {@code /* REVOKE … *}{@code /} pass.
 *
 * <p>This is the whole of the gated rule. GRANT/REVOKE inside {@code EXECUTE}/{@code DO} dynamic SQL
 * is not inspected (gap DG-E044-DYN-01); a future rule owns that, not this one.
 */
public final class GrantRule implements MigrationRule {

	private static final Pattern GRANT = Pattern.compile("(?i)\\s*(?:GRANT|REVOKE)\\b");

	@Override
	public String ruleId() {
		return "L-GRANT";
	}

	@Override
	public List<MigrationFinding> check(ParsedMigrationFile file, FolderContext folder) {
		TreeSet<Integer> lines = new TreeSet<>();
		List<String> codeLines = file.codeText().lines().toList();
		for (int index = 0; index < codeLines.size(); index++) {
			if (startsWithGrant(codeLines.get(index).stripLeading())) {
				lines.add(index + 1);
			}
		}
		for (MigrationStatement statement : file.statements()) {
			if (startsWithGrant(statement.firstWord())) {
				lines.add(statement.startLine());
			}
		}
		List<MigrationFinding> findings = new ArrayList<>();
		for (int line : lines) {
			findings.add(new MigrationFinding(ruleId(), file.fileName(), line, null,
					"GRANT/REVOKE belongs to the view story, not a recovery migration"));
		}
		return findings;
	}

	/** The inherited word-boundary match, {@code (?i)^\s*(grant|revoke)\b} (CONF-E044-03). */
	private static boolean startsWithGrant(String text) {
		return GRANT.matcher(text).lookingAt();
	}

}
