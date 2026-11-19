package th.co.scb.ace.demo.recovery.architecture.parameters;

import java.util.ArrayList;
import java.util.List;
import java.util.regex.Matcher;
import java.util.regex.Pattern;

/**
 * The token stream of {@link JavaLiteralTokenizer} turned into normalised numeric literals and
 * string literals with their line (SPEC-RWB-E1-042-004, finding 131). Normalising first means a
 * reformatted literal cannot slip past the ratchet; a number in a comment or a string is never a
 * literal.
 */
public final class MagicNumberScanner {

	/** A numeric literal as written and its normalised form. */
	public record NumberLiteral(String literal, int line, int offset) {
	}

	/** A string literal's text without delimiters. */
	public record StringLiteral(String text, int line) {
	}

	/** One scanned file. */
	public record Scan(String file, List<NumberLiteral> numbers, List<StringLiteral> strings) {

		public Scan {
			numbers = List.copyOf(numbers);
			strings = List.copyOf(strings);
		}
	}

	private static final Pattern NUMBER = Pattern.compile(
			"(?<![\\w$.])(-?)(0[xX][0-9a-fA-F_]+|\\d[\\d_]*(?:\\.[\\d_]+)?(?:[eE]-?\\d+)?)([fFdDlL])?");

	private MagicNumberScanner() {
	}

	public static Scan scan(String file, String source) {
		JavaLiteralTokenizer.Result tokenized = JavaLiteralTokenizer.tokenize(source);
		List<StringLiteral> strings = new ArrayList<>();
		for (JavaLiteralTokenizer.Token token : tokenized.literals()) {
			strings.add(new StringLiteral(token.text(), token.line()));
		}
		return new Scan(file, numbers(tokenized.masked()), strings);
	}

	public static List<NumberLiteral> numbers(String masked) {
		List<NumberLiteral> numbers = new ArrayList<>();
		Matcher matcher = NUMBER.matcher(masked);
		while (matcher.find()) {
			String raw = matcher.group(1) + matcher.group(2);
			numbers.add(new NumberLiteral(normalise(raw), lineOf(masked, matcher.start(2)), matcher.start(2)));
		}
		return List.copyOf(numbers);
	}

	static String normalise(String raw) {
		String value = raw.replace("_", "");
		boolean negative = value.startsWith("-");
		if (negative) {
			value = value.substring(1);
		}
		if (value.startsWith("0x") || value.startsWith("0X")) {
			value = "0x" + value.substring(2).toLowerCase();
		}
		else {
			int last = value.length() - 1;
			if (last >= 0 && "fFdDlL".indexOf(value.charAt(last)) >= 0) {
				value = value.substring(0, last);
			}
		}
		return negative ? "-" + value : value;
	}

	private static int lineOf(String text, int offset) {
		int line = 1;
		for (int i = 0; i < offset && i < text.length(); i++) {
			if (text.charAt(i) == '\n') {
				line++;
			}
		}
		return line;
	}
}
