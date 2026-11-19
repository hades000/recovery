package th.co.scb.ace.demo.recovery.architecture.parameters;

import java.util.ArrayList;
import java.util.List;

/**
 * One left-to-right pass over a Java source file (SPEC-RWB-E1-042-004, finding 131). Comments are
 * blanked; string, text-block and char literal bodies are kept as tokens; offsets and line numbers
 * are preserved so a finding names the real line.
 */
public final class JavaLiteralTokenizer {

	public enum Kind {
		STRING, TEXT_BLOCK, CHAR
	}

	/** One literal: its content without delimiters, its 1-based start line and its char offset. */
	public record Token(Kind kind, String text, int line, int offset) {
	}

	/** The comment- and literal-blanked source (same length) plus the literals in file order. */
	public record Result(String masked, List<Token> literals) {

		public Result {
			literals = List.copyOf(literals);
		}
	}

	private JavaLiteralTokenizer() {
	}

	public static Result tokenize(String source) {
		char[] masked = source.toCharArray();
		List<Token> literals = new ArrayList<>();
		int index = 0;
		int line = 1;
		int length = source.length();
		while (index < length) {
			char c = source.charAt(index);
			if (c == '/' && index + 1 < length && source.charAt(index + 1) == '/') {
				while (index < length && source.charAt(index) != '\n') {
					masked[index++] = ' ';
				}
				continue;
			}
			if (c == '/' && index + 1 < length && source.charAt(index + 1) == '*') {
				index = blankBlockComment(source, masked, index);
				line = countLines(source, 0, index) + 1;
				continue;
			}
			if (c == '"' && index + 2 < length && source.charAt(index + 1) == '"' && source.charAt(index + 2) == '"') {
				int start = index;
				int startLine = line;
				int contentStart = index + 3;
				int close = findTextBlockEnd(source, contentStart);
				int contentEnd = close < 0 ? length : close;
				literals.add(new Token(Kind.TEXT_BLOCK, source.substring(contentStart, contentEnd), startLine, start));
				int end = close < 0 ? length : close + 3;
				for (int i = start; i < end; i++) {
					if (masked[i] != '\n' && masked[i] != '\r') {
						masked[i] = ' ';
					}
				}
				line += countLines(source, start, end);
				index = end;
				continue;
			}
			if (c == '"') {
				index = readQuoted(source, masked, literals, index, '"', Kind.STRING, line);
				line = countLines(source, 0, index) + 1;
				continue;
			}
			if (c == '\'') {
				index = readQuoted(source, masked, literals, index, '\'', Kind.CHAR, line);
				line = countLines(source, 0, index) + 1;
				continue;
			}
			if (c == '\n') {
				line++;
			}
			index++;
		}
		return new Result(new String(masked), literals);
	}

	private static int findTextBlockEnd(String source, int from) {
		int index = from;
		while (index + 2 < source.length()) {
			if (source.charAt(index) == '\\') {
				index += 2;
				continue;
			}
			if (source.charAt(index) == '"' && source.charAt(index + 1) == '"' && source.charAt(index + 2) == '"') {
				return index;
			}
			index++;
		}
		return -1;
	}

	private static int blankBlockComment(String source, char[] masked, int start) {
		int index = start;
		int length = source.length();
		masked[index++] = ' ';
		if (index < length) {
			masked[index++] = ' ';
		}
		while (index < length) {
			if (source.charAt(index) == '*' && index + 1 < length && source.charAt(index + 1) == '/') {
				masked[index++] = ' ';
				if (index < length) {
					masked[index++] = ' ';
				}
				return index;
			}
			if (masked[index] != '\n' && masked[index] != '\r') {
				masked[index] = ' ';
			}
			index++;
		}
		return index;
	}

	private static int readQuoted(String source, char[] masked, List<Token> literals, int start, char delimiter,
			Kind kind, int line) {
		int index = start + 1;
		int length = source.length();
		StringBuilder text = new StringBuilder();
		masked[start] = ' ';
		while (index < length) {
			char c = source.charAt(index);
			if (c == '\\' && index + 1 < length) {
				text.append(c).append(source.charAt(index + 1));
				masked[index] = ' ';
				masked[index + 1] = ' ';
				index += 2;
				continue;
			}
			if (c == delimiter) {
				masked[index] = ' ';
				index++;
				literals.add(new Token(kind, unescape(text.toString()), line, start));
				return index;
			}
			if (c == '\n') {
				literals.add(new Token(kind, unescape(text.toString()), line, start));
				return index;
			}
			text.append(c);
			masked[index] = ' ';
			index++;
		}
		literals.add(new Token(kind, unescape(text.toString()), line, start));
		return index;
	}

	private static String unescape(String text) {
		StringBuilder out = new StringBuilder(text.length());
		for (int i = 0; i < text.length(); i++) {
			char c = text.charAt(i);
			if (c == '\\' && i + 1 < text.length()) {
				char next = text.charAt(++i);
				switch (next) {
					case 'n' -> out.append('\n');
					case 't' -> out.append('\t');
					case 'r' -> out.append('\r');
					case 'b' -> out.append('\b');
					case 'f' -> out.append('\f');
					case '0' -> out.append('\0');
					default -> out.append(next);
				}
			}
			else {
				out.append(c);
			}
		}
		return out.toString();
	}

	private static int countLines(String text, int from, int to) {
		int count = 0;
		for (int i = from; i < to && i < text.length(); i++) {
			if (text.charAt(i) == '\n') {
				count++;
			}
		}
		return count;
	}
}
