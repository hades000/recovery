package th.co.scb.ace.demo.recovery.architecture.migration;

import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Path;
import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.Map;

/**
 * SPEC-RWB-E1-044-007: one left-to-right, quote-aware pass over the raw file. Comments and strings
 * are never removed by separate passes or regular expressions, so a {@code /*} inside a literal or
 * a quote inside a comment cannot hide real code.
 *
 * <p>The pass produces three line-preserving views: the code text (comments blanked, strings kept),
 * the identifier text (comments and strings blanked, quoted identifiers and bodies kept as code) and
 * the statements cut at top-level {@code ;}. Blanked characters become spaces and newlines are kept,
 * so an offset means the same position in every view.
 */
public final class MigrationLexer {

	/** A migration file above this size is refused rather than tokenised (SEC-044-05). */
	public static final int MAX_CHARACTERS = 262_144;

	/** Dollar-quoted bodies may nest this deep; deeper input is refused (SEC-044-05). */
	public static final int MAX_DOLLAR_DEPTH = 32;

	private MigrationLexer() {
	}

	public static ParsedMigrationFile parse(Path path) throws IOException {
		String fileName = path.getFileName().toString();
		if (Files.size(path) > MAX_CHARACTERS) {
			throw new IllegalArgumentException(
					"migration file " + fileName + " is larger than " + MAX_CHARACTERS + " characters");
		}
		return parse(fileName, Files.readString(path));
	}

	public static ParsedMigrationFile parse(String fileName, String text) {
		if (text.length() > MAX_CHARACTERS) {
			throw new IllegalArgumentException(
					"migration file " + fileName + " is larger than " + MAX_CHARACTERS + " characters");
		}
		char[] code = text.toCharArray();
		char[] identifier = text.toCharArray();
		List<LexProblem> problems = new ArrayList<>();
		List<Integer> cuts = new ArrayList<>();
		int[] lineStarts = ParsedMigrationFile.lineStarts(text);
		new Pass(fileName, text, code, identifier, problems, cuts, lineStarts).scan(0, text.length(), false);
		String codeText = new String(code);
		String identifierText = new String(identifier);
		return new ParsedMigrationFile(fileName, text.lines().toList(), codeText, identifierText,
				statements(identifierText, cuts, lineStarts), problems);
	}

	private static List<MigrationStatement> statements(String identifierText, List<Integer> cuts, int[] lineStarts) {
		List<MigrationStatement> statements = new ArrayList<>();
		int start = 0;
		for (int cut : cuts) {
			addStatement(identifierText, start, cut, statements, lineStarts);
			start = cut + 1;
		}
		addStatement(identifierText, start, identifierText.length(), statements, lineStarts);
		return statements;
	}

	private static void addStatement(String identifierText, int start, int end, List<MigrationStatement> statements,
			int[] lineStarts) {
		int first = start;
		while (first < end && Character.isWhitespace(identifierText.charAt(first))) {
			first++;
		}
		if (first >= end) {
			return;
		}
		List<String> words = firstWords(identifierText.substring(first, end), 5);
		String firstWord = words.isEmpty() ? "" : words.get(0);
		statements.add(new MigrationStatement(first, end, ParsedMigrationFile.lineOf(lineStarts, first), firstWord,
				kind(words)));
	}

	/** {@code CREATE TABLE}, {@code CREATE OR REPLACE VIEW}, {@code GRANT}, ... */
	private static String kind(List<String> words) {
		if (words.isEmpty()) {
			return "";
		}
		if (!words.get(0).equals("CREATE")) {
			return words.get(0);
		}
		if (words.size() >= 4 && words.get(1).equals("OR") && words.get(2).equals("REPLACE")) {
			return "CREATE OR REPLACE " + words.get(3);
		}
		return words.size() >= 2 ? "CREATE " + words.get(1) : "CREATE";
	}

	private static List<String> firstWords(String text, int max) {
		List<String> words = new ArrayList<>();
		int i = 0;
		while (i < text.length() && words.size() < max) {
			while (i < text.length() && Character.isWhitespace(text.charAt(i))) {
				i++;
			}
			int start = i;
			while (i < text.length() && isIdentifierPart(text.charAt(i))) {
				i++;
			}
			if (start == i) {
				break;
			}
			words.add(text.substring(start, i).toUpperCase(java.util.Locale.ROOT));
		}
		return words;
	}

	private static boolean isIdentifierPart(char c) {
		return Character.isLetterOrDigit(c) || c == '_' || c == '$';
	}

	private static void blank(char[] view, int from, int to) {
		for (int i = from; i < to && i < view.length; i++) {
			char c = view[i];
			if (c != '\n' && c != '\r') {
				view[i] = ' ';
			}
		}
	}

	private static final class Pass {

		private final String fileName;

		private final String text;

		private final char[] code;

		private final char[] identifier;

		private final List<LexProblem> problems;

		private final List<Integer> cuts;

		private final int[] lineStarts;

		private int depth;

		private Map<Integer, Integer> blockCommentEnds;

		Pass(String fileName, String text, char[] code, char[] identifier, List<LexProblem> problems,
				List<Integer> cuts, int[] lineStarts) {
			this.fileName = fileName;
			this.text = text;
			this.code = code;
			this.identifier = identifier;
			this.problems = problems;
			this.cuts = cuts;
			this.lineStarts = lineStarts;
		}

		void scan(int from, int limit, boolean body) {
			int i = from;
			while (i < limit) {
				if (!body && text.charAt(i) == ';') {
					cuts.add(i);
					i++;
					continue;
				}
				if (startsWith("--", i, limit)) {
					int end = lineEnd(i, limit);
					blank(code, i, end);
					blank(identifier, i, end);
					i = end;
					continue;
				}
				if (startsWith("/*", i, limit)) {
					int end = blockCommentEnd(i, limit);
					if (end < 0) {
						i = unterminated(i, limit, body, "block comment", 2, true);
					}
					else {
						blank(code, i, end);
						blank(identifier, i, end);
						i = end;
					}
					continue;
				}
				int escape = escapeStringStart(i, limit);
				if (escape > 0) {
					i = string(i, escape, limit, body, "escape string", stringEnd(i + escape, limit, true));
					continue;
				}
				int standard = standardStringStart(i, limit);
				if (standard > 0) {
					i = string(i, standard, limit, body, "string", stringEnd(i + standard, limit, false));
					continue;
				}
				int quoted = quotedIdentifierStart(i, limit);
				if (quoted > 0) {
					int end = quotedIdentifierEnd(i + quoted, limit);
					if (end < 0) {
						i = unterminated(i, limit, body, "quoted identifier", quoted, false);
					}
					else {
						i = end;
					}
					continue;
				}
				if (startsWith("${", i, limit)) {
					int end = text.indexOf('}', i + 2);
					i = (end < 0 || end >= limit) ? i + 2 : end + 1;
					continue;
				}
				int tag = dollarTagLength(i, limit);
				if (tag > 0) {
					i = dollarBody(i, tag, limit, body);
					continue;
				}
				i++;
			}
		}

		private int dollarBody(int i, int tag, int limit, boolean body) {
			if (depth >= MAX_DOLLAR_DEPTH) {
				throw new IllegalArgumentException("migration file " + fileName
						+ " exceeds the dollar-quote nesting limit of " + MAX_DOLLAR_DEPTH);
			}
			String delimiter = text.substring(i, i + tag);
			int end = text.indexOf(delimiter, i + tag);
			if (end < 0 || end + tag > limit) {
				return unterminated(i, limit, body, "dollar-quoted body", tag, false);
			}
			blank(identifier, i, i + tag);
			blank(identifier, end, end + tag);
			depth++;
			try {
				scan(i + tag, end, true);
			}
			finally {
				depth--;
			}
			return end + tag;
		}

		/**
		 * The opener is treated as one code character and tokenizing resumes after it, so the rest
		 * of the file is still checked. Inside a body the body end always wins: the token is blanked
		 * to the limit and no problem is recorded.
		 */
		private int unterminated(int i, int limit, boolean body, String kind, int openerLength, boolean blankBoth) {
			if (body) {
				if (blankBoth) {
					blank(code, i, limit);
				}
				blank(identifier, i, limit);
				return limit;
			}
			problems.add(new LexProblem(kind, ParsedMigrationFile.lineOf(lineStarts, i), i));
			return i + openerLength;
		}

		private int string(int i, int openerLength, int limit, boolean body, String kind, int end) {
			if (end < 0) {
				return unterminated(i, limit, body, kind, openerLength, false);
			}
			blank(identifier, i, end);
			return end;
		}

		private int stringEnd(int start, int limit, boolean escaped) {
			int i = start;
			while (i < limit) {
				char c = text.charAt(i);
				if (escaped && c == '\\') {
					i += 2;
					continue;
				}
				if (c == '\'') {
					if (i + 1 < limit && text.charAt(i + 1) == '\'') {
						i += 2;
						continue;
					}
					return i + 1;
				}
				i++;
			}
			return -1;
		}

		private int quotedIdentifierEnd(int start, int limit) {
			int i = start;
			while (i < limit) {
				if (text.charAt(i) == '"') {
					if (i + 1 < limit && text.charAt(i + 1) == '"') {
						i += 2;
						continue;
					}
					return i + 1;
				}
				i++;
			}
			return -1;
		}

		/**
		 * The matching close of a block comment, computed once for the whole file with a stack.
		 * Every query starts at a real {@code /*} opener, and inside a comment only {@code /*} and
		 * {@code *}{@code /} are recognised, so one pass gives the same answer as rescanning from
		 * each opener, without the quadratic rescan (SEC-044-05). A match beyond {@code limit} is
		 * unterminated for that bounded body.
		 */
		private int blockCommentEnd(int from, int limit) {
			if (blockCommentEnds == null) {
				blockCommentEnds = matchBlockComments();
			}
			Integer end = blockCommentEnds.get(from);
			return end != null && end <= limit ? end : -1;
		}

		private Map<Integer, Integer> matchBlockComments() {
			Map<Integer, Integer> ends = new HashMap<>();
			java.util.Deque<Integer> openers = new java.util.ArrayDeque<>();
			int i = 0;
			while (i + 1 < text.length()) {
				if (text.charAt(i) == '/' && text.charAt(i + 1) == '*') {
					openers.push(i);
					i += 2;
					continue;
				}
				if (text.charAt(i) == '*' && text.charAt(i + 1) == '/') {
					if (!openers.isEmpty()) {
						ends.put(openers.pop(), i + 2);
					}
					i += 2;
					continue;
				}
				i++;
			}
			return ends;
		}

		private int lineEnd(int from, int limit) {
			int i = from;
			while (i < limit && text.charAt(i) != '\n') {
				i++;
			}
			return i;
		}

		private int escapeStringStart(int i, int limit) {
			char c = text.charAt(i);
			if (c != 'E' && c != 'e') {
				return 0;
			}
			if (i + 1 >= limit || text.charAt(i + 1) != '\'') {
				return 0;
			}
			return i > 0 && isIdentifierPart(text.charAt(i - 1)) ? 0 : 2;
		}

		private int standardStringStart(int i, int limit) {
			char c = text.charAt(i);
			if (c == '\'') {
				return 1;
			}
			boolean plainPrefix = i + 1 < limit && text.charAt(i + 1) == '\'' && "BbXxNn".indexOf(c) >= 0;
			boolean unicodePrefix = i + 2 < limit && (c == 'U' || c == 'u') && text.charAt(i + 1) == '&'
					&& text.charAt(i + 2) == '\'';
			if (!plainPrefix && !unicodePrefix) {
				return 0;
			}
			if (i > 0 && isIdentifierPart(text.charAt(i - 1))) {
				return 0;
			}
			return unicodePrefix ? 3 : 2;
		}

		private int quotedIdentifierStart(int i, int limit) {
			char c = text.charAt(i);
			if (c == '"') {
				return 1;
			}
			boolean unicodePrefix = i + 2 < limit && (c == 'U' || c == 'u') && text.charAt(i + 1) == '&'
					&& text.charAt(i + 2) == '"';
			if (!unicodePrefix || (i > 0 && isIdentifierPart(text.charAt(i - 1)))) {
				return 0;
			}
			return 3;
		}

		private int dollarTagLength(int i, int limit) {
			if (text.charAt(i) != '$') {
				return 0;
			}
			if (i > 0 && isIdentifierPart(text.charAt(i - 1))) {
				return 0;
			}
			int j = i + 1;
			if (j < limit && text.charAt(j) == '$') {
				return 2;
			}
			if (j < limit && (Character.isLetter(text.charAt(j)) || text.charAt(j) == '_')) {
				j++;
				while (j < limit && (Character.isLetterOrDigit(text.charAt(j)) || text.charAt(j) == '_')) {
					j++;
				}
				if (j < limit && text.charAt(j) == '$') {
					return j - i + 1;
				}
			}
			return 0;
		}

		private boolean startsWith(String token, int i, int limit) {
			return i + token.length() <= limit && text.startsWith(token, i);
		}
	}
}
