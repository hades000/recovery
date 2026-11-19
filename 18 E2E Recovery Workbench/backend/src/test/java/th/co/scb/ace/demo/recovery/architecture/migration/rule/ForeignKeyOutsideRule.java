package th.co.scb.ace.demo.recovery.architecture.migration.rule;

import java.util.LinkedHashMap;
import java.util.List;
import java.util.Locale;
import java.util.Map;
import java.util.regex.Matcher;
import java.util.regex.Pattern;

import th.co.scb.ace.demo.recovery.architecture.migration.FolderContext;
import th.co.scb.ace.demo.recovery.architecture.migration.MigrationFinding;
import th.co.scb.ace.demo.recovery.architecture.migration.MigrationRule;
import th.co.scb.ace.demo.recovery.architecture.migration.ParsedMigrationFile;

/**
 * SPEC-RWB-E1-044-008 (T-044-05, BR8): {@code REFERENCES <qualifier>.<table>} fails unless the
 * qualifier is {@code ${recoverySchema}}. An unqualified reference passes. This rule never consults
 * {@link LiteralSchemaRule#isAllowedQualifier}, so the SEAM-E044-01 exception cannot reach it.
 */
public final class ForeignKeyOutsideRule implements MigrationRule {

	private static final Pattern REFERENCES = Pattern
		.compile("(?i)\\bREFERENCES\\s+(\\$\\{[^}]*\\}|\"([^\"]+)\"|([A-Za-z_][A-Za-z0-9_$]*))\\s*\\.");

	@Override
	public String ruleId() {
		return "L-FK-OUTSIDE";
	}

	@Override
	public List<MigrationFinding> check(ParsedMigrationFile file, FolderContext folder) {
		String text = file.identifierText();
		Map<String, MigrationFinding> findings = new LinkedHashMap<>();
		Matcher matcher = REFERENCES.matcher(text);
		while (matcher.find()) {
			String qualifier = name(matcher);
			if (!"${recoverySchema}".equals(qualifier)) {
				int line = file.lineOf(matcher.start(1));
				findings.putIfAbsent(line + "|" + qualifier, new MigrationFinding(ruleId(), file.fileName(), line,
						qualifier, "BR8 foreign key outside recovery schema"));
			}
		}
		return List.copyOf(findings.values());
	}

	private static String name(Matcher matcher) {
		if (matcher.group(2) != null) {
			return matcher.group(2);
		}
		if (matcher.group(3) != null) {
			return matcher.group(3).toLowerCase(Locale.ROOT);
		}
		return matcher.group(1);
	}

}
