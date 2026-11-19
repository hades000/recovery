package th.co.scb.ace.demo.recovery.casewf.config;

import java.util.ArrayList;
import java.util.List;

/**
 * RFC 4180 CSV reader shared by the catalog parser and the parameter load file (SPEC-RWB-E1-042-003,
 * -012). A quoted field may hold a comma, a doubled quote or a line break; the line of each row is
 * the 1-based line on which it starts, so a finding can name it.
 */
public final class CsvRows {

	/** One logical CSV row and the physical line it starts on. */
	public record Row(int line, List<String> fields) {

		public Row {
			fields = List.copyOf(fields);
		}

		public String field(int index) {
			return index < fields.size() ? fields.get(index) : "";
		}
	}

	/** A malformed CSV document; the line is 1-based. */
	public static final class CsvFormatException extends RuntimeException {

		private final int line;

		CsvFormatException(int line, String message) {
			super(message);
			this.line = line;
		}

		public int line() {
			return line;
		}
	}

	private CsvRows() {
	}

	public static List<Row> parse(String text) {
		List<Row> rows = new ArrayList<>();
		String source = stripBom(text);
		int line = 1;
		int index = 0;
		int length = source.length();
		while (index < length) {
			int rowLine = line;
			List<String> fields = new ArrayList<>();
			StringBuilder field = new StringBuilder();
			boolean quoted = false;
			boolean closed = false;
			boolean rowEnded = false;
			while (index < length && !rowEnded) {
				char c = source.charAt(index);
				if (quoted) {
					if (c == '"') {
						if (index + 1 < length && source.charAt(index + 1) == '"') {
							field.append('"');
							index += 2;
							continue;
						}
						quoted = false;
						closed = true;
						index++;
						continue;
					}
					if (c == '\n') {
						line++;
					}
					field.append(c);
					index++;
					continue;
				}
				if (closed && c != ',' && c != '\n' && c != '\r') {
					throw new CsvFormatException(line, "unexpected character after a closing quote");
				}
				switch (c) {
					case '"' -> {
						if (!field.isEmpty()) {
							throw new CsvFormatException(line, "quote inside an unquoted field");
						}
						quoted = true;
						index++;
					}
					case ',' -> {
						fields.add(field.toString());
						field.setLength(0);
						closed = false;
						index++;
					}
					case '\r' -> {
						index++;
						if (index < length && source.charAt(index) == '\n') {
							index++;
						}
						fields.add(field.toString());
						rowEnded = true;
						line++;
					}
					case '\n' -> {
						index++;
						fields.add(field.toString());
						rowEnded = true;
						line++;
					}
					default -> {
						field.append(c);
						index++;
					}
				}
			}
			if (quoted) {
				throw new CsvFormatException(rowLine, "unterminated quoted field");
			}
			if (!rowEnded) {
				fields.add(field.toString());
			}
			if (isBlankRow(fields)) {
				continue;
			}
			rows.add(new Row(rowLine, fields));
		}
		return List.copyOf(rows);
	}

	private static boolean isBlankRow(List<String> fields) {
		return fields.isEmpty() || fields.stream().allMatch(String::isBlank);
	}

	private static String stripBom(String text) {
		return text != null && text.startsWith("\uFEFF") ? text.substring(1) : text;
	}
}
