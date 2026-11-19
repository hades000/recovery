package th.co.scb.ace.demo.recovery.architecture.migration;

import java.util.List;
import java.util.regex.Matcher;
import java.util.regex.Pattern;

/**
 * SPEC-RWB-E1-044-007: the parsed migration file. Every rule reads these views, so all rules share
 * one tokenizer pass. {@code codeText} and {@code identifierText} keep the raw text's length and
 * line structure, so an offset means the same position in both.
 */
public final class ParsedMigrationFile {

	/** D-RCV-28 (1): the only accepted migration name. */
	static final Pattern NAME = Pattern.compile("^V(\\d{4})__(rwb_[a-z0-9]+_\\d{3})_[a-z0-9_]+\\.sql$");

	/** The numeric prefix still orders a file whose story token is malformed (L-NAME reports it). */
	private static final Pattern VERSIONED = Pattern.compile("^V(\\d{4})__.*\\.sql$");

	private final String fileName;

	private final List<String> rawLines;

	private final String codeText;

	private final String identifierText;

	private final List<MigrationStatement> statements;

	private final List<LexProblem> unterminated;

	private final int[] lineStarts;

	ParsedMigrationFile(String fileName, List<String> rawLines, String codeText, String identifierText,
			List<MigrationStatement> statements, List<LexProblem> unterminated) {
		this.fileName = fileName;
		this.rawLines = List.copyOf(rawLines);
		this.codeText = codeText;
		this.identifierText = identifierText;
		this.statements = List.copyOf(statements);
		this.unterminated = List.copyOf(unterminated);
		this.lineStarts = lineStarts(codeText);
	}

	/** The 1-based line of an offset in either same-length view. */
	public int lineOf(int offset) {
		return lineOf(lineStarts, offset);
	}

	static int[] lineStarts(String text) {
		int lines = 1;
		for (int i = 0; i < text.length(); i++) {
			if (text.charAt(i) == '\n') {
				lines++;
			}
		}
		int[] starts = new int[lines];
		int line = 1;
		for (int i = 0; i < text.length(); i++) {
			if (text.charAt(i) == '\n') {
				starts[line++] = i + 1;
			}
		}
		return starts;
	}

	static int lineOf(int[] lineStarts, int offset) {
		int index = java.util.Arrays.binarySearch(lineStarts, offset);
		return (index >= 0 ? index : -index - 2) + 1;
	}

	public String fileName() {
		return fileName;
	}

	public List<String> rawLines() {
		return rawLines;
	}

	/** View (a): comments blanked, strings and quoted identifiers kept. */
	public String codeText() {
		return codeText;
	}

	/** View (b): comments and strings blanked, quoted identifiers and bodies kept as code. */
	public String identifierText() {
		return identifierText;
	}

	/** View (c): statement ranges over the identifier text. */
	public List<MigrationStatement> statements() {
		return statements;
	}

	public List<LexProblem> unterminated() {
		return unterminated;
	}

	public boolean hasVersionedName() {
		return NAME.matcher(fileName).matches();
	}

	/** The four-digit sequence, or -1 when the name has no {@code V<seq>__} prefix. */
	public int sequence() {
		Matcher matcher = VERSIONED.matcher(fileName);
		return matcher.matches() ? Integer.parseInt(matcher.group(1)) : -1;
	}

	/** The story token from the name, for example {@code rwb_e1_044}, or null. */
	public String storyToken() {
		Matcher matcher = NAME.matcher(fileName);
		return matcher.matches() ? matcher.group(2) : null;
	}

	/** The story key derived from the name, for example {@code RWB-E1-044}, or null. */
	public String storyKey() {
		String token = storyToken();
		return token == null ? null : token.toUpperCase(java.util.Locale.ROOT).replace('_', '-');
	}

	/** D-RCV-28: a corrective file has {@code -- Fix:} as the first text of line 2. */
	public boolean isFix() {
		return rawLines.size() > 1 && rawLines.get(1).startsWith("-- Fix:");
	}

	public static boolean isRepeatableName(String name) {
		return name.startsWith("R__") && name.endsWith(".sql");
	}

	public static boolean isUndoName(String name) {
		return name.startsWith("U") && name.endsWith(".sql");
	}
}
