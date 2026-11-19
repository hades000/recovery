package th.co.scb.ace.demo.recovery.architecture.migration.rule;

import java.util.Comparator;
import java.util.LinkedHashMap;
import java.util.List;
import java.util.Locale;
import java.util.Map;
import java.util.Set;
import java.util.regex.Matcher;
import java.util.regex.Pattern;

import th.co.scb.ace.demo.recovery.architecture.migration.FolderContext;
import th.co.scb.ace.demo.recovery.architecture.migration.MigrationFinding;
import th.co.scb.ace.demo.recovery.architecture.migration.MigrationRule;
import th.co.scb.ace.demo.recovery.architecture.migration.MigrationStatement;
import th.co.scb.ace.demo.recovery.architecture.migration.ParsedMigrationFile;

/**
 * SPEC-RWB-E1-044-007, -016 (T-044-02, -21, AC5): a literal schema qualifier fails, unless it is
 * {@code ${recoverySchema}}, {@code information_schema} or {@code pg_catalog}.
 *
 * <p>The rule runs on the identifier text, so a comment or a string literal never hides a real
 * reference. Items 1 to 4 are ways of finding one disallowed name, not separate findings: the rule
 * reports once per (file, line, schema name) (SPEC-004). Item 1 matches positions lexically, so an
 * alias or record qualifier after {@code FROM} or {@code INTO} is reported and this fails closed
 * (ASM-E044-06).
 *
 * <p>{@link #isAllowedQualifier(MigrationStatement, String)} is the single extension point a later
 * story uses (SEAM-E044-01, owner RWB-E1-069). No {@code public} exception is built here.
 */
public final class LiteralSchemaRule implements MigrationRule {
	private static final Set<String> KNOWN_SCHEMAS = Set.of("recovery", "ace", "public");

	/**
	 * A keyword boundary in which {@code $} is part of a name, as in PostgreSQL: {@code \b} would split
	 * {@code idx$on} and read its {@code on} as the keyword (CONF4-E044-01).
	 */
	private static final String B = "(?:(?<![\\w$])(?=[\\w$])|(?<=[\\w$])(?![\\w$]))";

	private static final String QUALIFIER = "(\\$\\{[^}]*\\}|\"([^\"]+)\"|([A-Za-z_][A-Za-z0-9_$]*))";

	/** Item 4 and every qualified name: the qualifier of {@code a.b}. */
	private static final Pattern QUALIFIED = Pattern.compile("(?<![\\w$\"])" + QUALIFIER + "\\s*\\.");

	/**
	 * Items 1 and 2: a name in an object-name position, a qualified type, or {@code ::}.
	 * A bare {@code ON} is not a position: it is matched only by {@link #ON_OBJECT}, so a join condition
	 * {@code ON a.id} passes.
	 */
	private static final Pattern POSITION = Pattern
		.compile("(?i)(?:" + B + "(?:TABLE|VIEW|SEQUENCE|FUNCTION|PROCEDURE|TYPE|DOMAIN|REFERENCES|FROM|JOIN|INTO|"
				+ "UPDATE|TRUNCATE|OWNED\\s+BY|AS)" + B + "|::)\\s*" + QUALIFIER + "\\s*\\.");

	/**
	 * Item 1, the object name after {@code ON} in {@code INDEX … ON}, {@code TRIGGER … ON},
	 * {@code POLICY … ON}, {@code ALTER}/{@code DROP RULE … ON} and {@code GRANT}/{@code REVOKE … ON}
	 * (CONF-E044-07). Only the first {@code ON} after the prefix is the object name, so a later join
	 * {@code ON a.id} passes (CONF2-E044-03). A quoted identifier is skipped whole, so a word {@code on}
	 * inside it is not that {@code ON} (CONF3-E044-01). {@code CREATE RULE} is {@link #RULE_TO}: its
	 * {@code ON} names an event, not an object.
	 */
	private static final Pattern ON_OBJECT = Pattern.compile("(?i)(?:" + B + "(?:CREATE|ALTER|DROP)\\s+"
			+ "(?:(?:UNIQUE|OR\\s+REPLACE|CONSTRAINT)\\s+)*(?:INDEX|TRIGGER|POLICY)|" + B + "(?:ALTER|DROP)\\s+RULE|"
			+ B + "(?:GRANT|REVOKE))" + B + "(?:\"(?:[^\"]|\"\")*\"|(?!" + B + "ON" + B + ")[^;\"])*" + B
			+ "ON\\s+(?:ONLY\\s+)?" + QUALIFIER
			+ "\\s*\\.");

	/** A column or table name: plain, or quoted with {@code ""} escapes. */
	private static final String NAME = "(?:\"(?:[^\"]|\"\")+\"|[A-Za-z_][A-Za-z0-9_$]*)";

	/** Item 1, the table of {@code CREATE [OR REPLACE] RULE r AS ON <event> TO s.t} (CONF3-E044-02). */
	private static final Pattern RULE_TO = Pattern.compile("(?i)" + B + "CREATE\\s+(?:OR\\s+REPLACE\\s+)?RULE\\s+" + NAME
			+ "\\s+AS\\s+ON\\s+[A-Za-z]+\\s+TO\\s+" + QUALIFIER + "\\s*\\.");

	/**
	 * Item 1, {@code COMMENT ON <kind>} for every kind (CONF2-E044-01): the first qualified name within
	 * the kind words and the {@code … ON [DOMAIN]} forms, for example {@code INDEX}, {@code AGGREGATE},
	 * {@code TEXT SEARCH CONFIGURATION} or {@code CONSTRAINT k ON DOMAIN}. The comment text is a string,
	 * blanked in the identifier text, so the match cannot run past {@code IS}. {@code COLUMN} is
	 * {@link #COMMENT_COLUMN}.
	 */
	private static final Pattern COMMENT_ON = Pattern
		.compile("(?i)" + B + "COMMENT\\s+ON\\s+(?!COLUMN" + B + ")(?:" + NAME + "\\s+){1,4}?" + QUALIFIER + "\\s*\\.");

	/**
	 * Item 1, {@code COMMENT ON COLUMN s.t.c}: only a three-part name has a schema; in {@code t.c} the
	 * first part is the table (CONF2-E044-02).
	 */
	private static final Pattern COMMENT_COLUMN = Pattern
		.compile("(?i)" + B + "COMMENT\\s+ON\\s+COLUMN\\s+" + QUALIFIER + "\\s*\\.\\s*" + NAME + "\\s*\\.");

	/** Item 2, column data type in {@code ALTER TABLE ... ADD [COLUMN] [IF NOT EXISTS] c type}. */
	private static final Pattern ADD_COLUMN = Pattern.compile(
			"(?i)" + B + "ADD\\s+(?:COLUMN\\s+)?(?:IF\\s+NOT\\s+EXISTS\\s+)?" + NAME + "\\s+" + QUALIFIER + "\\s*\\.");

	/** The opening parenthesis of a {@code CREATE TABLE} column list. */
	private static final Pattern TABLE_OPEN = Pattern.compile("(?i)" + B
			+ "TABLE\\s+(?:IF\\s+NOT\\s+EXISTS\\s+)?(?:(?:\\$\\{[^}]*\\}|"
			+ NAME + ")\\s*\\.\\s*)?" + NAME + "\\s*\\(");

	/** Item 2, column data type: one element of a column list, {@code c type}. */
	private static final Pattern COLUMN_TYPE = Pattern.compile("\\s*" + NAME + "\\s+" + QUALIFIER + "\\s*\\.");

	/** Item 3: a bare schema name. */
	private static final Pattern BARE_SCHEMA = Pattern.compile("(?i)" + B + "SCHEMA\\s+" + QUALIFIER);

	@Override
	public String ruleId() {
		return "L-LITERAL-SCHEMA";
	}

	@Override
	public List<MigrationFinding> check(ParsedMigrationFile file, FolderContext folder) {
		String text = file.identifierText();
		Map<String, MigrationFinding> findings = new LinkedHashMap<>();
		collect(findings, file, text, QUALIFIED, true);
		collect(findings, file, text, POSITION, false);
		collect(findings, file, text, ON_OBJECT, false);
		collect(findings, file, text, RULE_TO, false);
		collect(findings, file, text, COMMENT_ON, false);
		collect(findings, file, text, COMMENT_COLUMN, false);
		collect(findings, file, text, ADD_COLUMN, false);
		collectColumnTypes(findings, file, text);
		collect(findings, file, text, BARE_SCHEMA, false);
		return findings.values().stream().sorted(Comparator.comparingInt(MigrationFinding::line)).toList();
	}

	/**
	 * The patterns are applied to the whole identifier text, not per line, so whitespace (including
	 * a newline) or a comment between the qualifier and its dot does not hide the reference
	 * (SEC-044-02). The finding keeps the qualifier's own line and the (line, name) identity.
	 */
	private void collect(Map<String, MigrationFinding> findings, ParsedMigrationFile file, String text,
			Pattern pattern, boolean knownOnly) {
		Matcher matcher = pattern.matcher(text);
		while (matcher.find()) {
			report(findings, file, matcher, knownOnly);
		}
	}

	/**
	 * CONF-E044-02: each top-level element of a {@code CREATE TABLE} column list is checked for
	 * {@code c qualifier.type}. Nested parentheses ({@code numeric(18, 2)}, {@code CHECK (...)}) are
	 * skipped, so an expression is never read as a column definition.
	 */
	private void collectColumnTypes(Map<String, MigrationFinding> findings, ParsedMigrationFile file, String text) {
		Matcher table = TABLE_OPEN.matcher(text);
		Matcher column = COLUMN_TYPE.matcher(text);
		while (table.find()) {
			int depth = 0;
			int start = table.end();
			for (int i = table.end() - 1; i < text.length(); i++) {
				char c = text.charAt(i);
				if (c == '(') {
					depth++;
				}
				else if (depth == 1 && (c == ',' || c == ')')) {
					if (column.region(start, i).lookingAt()) {
						report(findings, file, column, false);
					}
					if (c == ')') {
						break;
					}
					start = i + 1;
				}
				else if (c == ')') {
					depth--;
				}
			}
		}
	}

	private void report(Map<String, MigrationFinding> findings, ParsedMigrationFile file, Matcher matcher,
			boolean knownOnly) {
		String name = name(matcher);
		if (knownOnly && !KNOWN_SCHEMAS.contains(name)) {
			return;
		}
		int line = file.lineOf(matcher.start(1));
		if (!knownOnly && isAllowedQualifier(statementAt(file, matcher.start(1)), name)) {
			return;
		}
		findings.putIfAbsent(line + "|" + name,
				new MigrationFinding(ruleId(), file.fileName(), line, name, "literal schema " + name));
	}

	/** The statement whose identifier-view offset range owns the qualifier (SPEC-016 seam). */
	static MigrationStatement statementAt(ParsedMigrationFile file, int offset) {
		for (MigrationStatement statement : file.statements()) {
			if (offset >= statement.startOffset() && offset < statement.endOffset()) {
				return statement;
			}
		}
		return null;
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

	/**
	 * SPEC-RWB-E1-044-016: the one decision point for an allowed qualifier. RWB-E1-069 adds its
	 * narrow {@code public} exception here (SEAM-E044-01); nothing else changes.
	 */
	public static boolean isAllowedQualifier(MigrationStatement statement, String qualifier) {
		return "${recoverySchema}".equals(qualifier) || "information_schema".equals(qualifier)
				|| "pg_catalog".equals(qualifier);
	}

}
