package th.co.scb.ace.demo.recovery.architecture.parameters;

import java.io.IOException;
import java.io.UncheckedIOException;
import java.nio.charset.StandardCharsets;
import java.nio.file.Files;
import java.nio.file.Path;
import java.util.ArrayList;
import java.util.LinkedHashMap;
import java.util.List;
import java.util.Map;
import java.util.Set;
import java.util.stream.Stream;

/**
 * The magic-number ratchet of SPEC-RWB-E1-042-004 and §12.11: a numeric literal that equals a
 * catalog default, or a string literal that equals a non-secret catalog default, fails unless the
 * reviewed baseline names it with a reason and an owner. {@code 0}, {@code 1} and {@code -1} are
 * allowed. A baseline entry whose literal is gone is stale and fails too.
 */
public final class MagicNumberBaseline {

	/** One reviewed allowance: a literal in a file, how often, why and who owns it. */
	public record Entry(String path, String literal, int count, String reason, String owner) {
	}

	/** One finding: where, which literal and what it collides with. */
	public record Finding(String file, int line, String literal, String message) {

		@Override
		public String toString() {
			return file + ":" + line + ": " + message;
		}
	}

	private static final Set<String> ALLOWED = Set.of("0", "1", "-1");

	private MagicNumberBaseline() {
	}

	public static List<Entry> read(Path baselineCsv) {
		List<Entry> entries = new ArrayList<>();
		for (String line : lines(baselineCsv)) {
			if (line.isBlank() || line.startsWith("path,")) {
				continue;
			}
			List<String> cells = splitCsv(line);
			if (cells.size() < 5) {
				throw new IllegalStateException("baseline row needs five columns: " + line);
			}
			entries.add(new Entry(cells.get(0), cells.get(1), Integer.parseInt(cells.get(2).trim()), cells.get(3),
					cells.get(4)));
		}
		return List.copyOf(entries);
	}

	public static List<Finding> check(Path sourceRoot, List<Entry> baseline, CatalogFileParser.Result catalog) {
		Map<String, String> numericDefaults = new LinkedHashMap<>();
		Map<String, String> stringDefaults = new LinkedHashMap<>();
		for (CatalogRow row : catalog.rows()) {
			if (row.secret() || row.defaultValue().isBlank()) {
				continue;
			}
			switch (row.valueType()) {
				case "INTEGER" -> numericDefaults.putIfAbsent(row.defaultValue(), row.key());
				case "DECIMAL" -> numericDefaults.putIfAbsent(new java.math.BigDecimal(row.defaultValue()).stripTrailingZeros()
					.toPlainString(), row.key());
				default -> stringDefaults.putIfAbsent(row.defaultValue(), row.key());
			}
		}
		Map<String, Integer> seen = new LinkedHashMap<>();
		List<Finding> findings = new ArrayList<>();
		for (Path file : javaFiles(sourceRoot)) {
			String relative = sourceRoot.relativize(file).toString().replace('\\', '/');
			MagicNumberScanner.Scan scan = MagicNumberScanner.scan(relative, readFile(file));
			for (MagicNumberScanner.NumberLiteral number : scan.numbers()) {
				if (ALLOWED.contains(number.literal())) {
					continue;
				}
				seen.merge(relative + "|" + number.literal(), 1, Integer::sum);
				String key = numericDefaults.get(number.literal());
				boolean baselined = baselined(baseline, relative, number.literal());
				if (key != null && !baselined) {
					findings.add(new Finding(relative, number.line(), number.literal(),
							"literal " + number.literal() + " matches catalog key " + key));
				}
				else if (key == null && !baselined) {
					findings.add(new Finding(relative, number.line(), number.literal(),
							"literal " + number.literal() + " is not in the baseline"));
				}
			}
			for (MagicNumberScanner.StringLiteral string : scan.strings()) {
				String key = stringDefaults.get(string.text());
				if (key == null) {
					continue;
				}
				seen.merge(relative + "|" + string.text(), 1, Integer::sum);
				if (!baselined(baseline, relative, string.text())) {
					findings.add(new Finding(relative, string.line(), string.text(),
							"string literal equals the default of catalog key " + key));
				}
			}
		}
		for (Entry entry : baseline) {
			Integer count = seen.get(entry.path() + "|" + entry.literal());
			if (count == null) {
				findings.add(new Finding(entry.path(), 0, entry.literal(),
						"baseline entry is stale: " + entry.literal() + " is no longer present"));
			}
			else if (count != entry.count()) {
				findings.add(new Finding(entry.path(), 0, entry.literal(),
						"baseline entry counts " + entry.count() + " but the code has " + count));
			}
		}
		return List.copyOf(findings);
	}

	private static boolean baselined(List<Entry> baseline, String path, String literal) {
		return baseline.stream().anyMatch(entry -> entry.path().equals(path) && entry.literal().equals(literal));
	}

	private static List<String> splitCsv(String line) {
		List<String> cells = new ArrayList<>();
		StringBuilder cell = new StringBuilder();
		boolean quoted = false;
		for (int i = 0; i < line.length(); i++) {
			char c = line.charAt(i);
			if (quoted) {
				if (c == '"' && i + 1 < line.length() && line.charAt(i + 1) == '"') {
					cell.append('"');
					i++;
				}
				else if (c == '"') {
					quoted = false;
				}
				else {
					cell.append(c);
				}
			}
			else if (c == '"') {
				quoted = true;
			}
			else if (c == ',') {
				cells.add(cell.toString());
				cell.setLength(0);
			}
			else {
				cell.append(c);
			}
		}
		cells.add(cell.toString());
		return cells;
	}

	private static List<String> lines(Path file) {
		try {
			return Files.readAllLines(file, StandardCharsets.UTF_8);
		}
		catch (IOException ex) {
			throw new UncheckedIOException(ex);
		}
	}

	private static String readFile(Path file) {
		try {
			return Files.readString(file, StandardCharsets.UTF_8);
		}
		catch (IOException ex) {
			throw new UncheckedIOException(ex);
		}
	}

	private static List<Path> javaFiles(Path root) {
		try (Stream<Path> files = Files.walk(root)) {
			return files.filter(path -> path.toString().endsWith(".java")).sorted().toList();
		}
		catch (IOException ex) {
			throw new UncheckedIOException(ex);
		}
	}

}
