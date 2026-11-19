package th.co.scb.ace.demo.recovery.architecture.parameters;

import java.io.IOException;
import java.io.UncheckedIOException;
import java.nio.charset.StandardCharsets;
import java.nio.file.Files;
import java.nio.file.Path;
import java.util.ArrayList;
import java.util.LinkedHashMap;
import java.util.LinkedHashSet;
import java.util.List;
import java.util.Locale;
import java.util.Map;
import java.util.Set;
import java.util.regex.Matcher;
import java.util.regex.Pattern;
import java.util.stream.Stream;

/**
 * The completeness rules of SPEC-RWB-E1-042-003, -005 and §12.11 of the spec: every key read in
 * recovery main code is catalogued, every row is complete, and a persisted row equals its catalog
 * row.
 *
 * <p>The reader-call rule is a source-level rule on the {@link JavaLiteralTokenizer} token stream.
 * It refuses a reader call whose first argument is not one string literal, a method reference, a
 * {@code var} local initialised from a reader, and a name declared both as a reader and with another
 * type. {@code Map.get} and {@code Optional.get} are not key reads. The file
 * {@code casewf/config/CatalogParameterReaderImpl.java} is skipped by path, because it implements
 * the reader and must call {@code ParameterService}.
 */
public final class CatalogCompletenessRules {

	/** One refusal: the file it was found in (relative to the scanned root), its line and the text. */
	public record Finding(String file, int line, String message) {

		@Override
		public String toString() {
			return file + ":" + line + ": " + message;
		}
	}

	private static final String READER = "CatalogParameterReader";

	private static final String EXEMPT_SUFFIX = "casewf/config/CatalogParameterReaderImpl.java";

	private static final Pattern READER_DECLARATION = Pattern.compile("\\b" + READER + "\\s+([A-Za-z_][A-Za-z0-9_]*)");

	private static final Pattern PARAMETER_KEYS_CONSTANT = Pattern.compile("\\bParameterKeys\\s*\\.\\s*([A-Z][A-Z0-9_]*)");

	private static final Pattern PARAMETER_KEY_OF = Pattern.compile("\\bParameterKey\\s*\\.\\s*of\\s*\\(");

	private static final Pattern STATIC_READER_GET = Pattern.compile("\\b" + READER + "\\s*\\.\\s*get\\s*\\(");

	private static final Pattern STATIC_READER_REFERENCE = Pattern.compile("\\b" + READER + "\\s*::\\s*get\\b");

	private CatalogCompletenessRules() {
	}

	/** Rule 1 and the refused forms of the reader-call rule. */
	public static List<Finding> keyReads(Path sourceRoot, CatalogFileParser.Result catalog) {
		Set<String> keys = new LinkedHashSet<>();
		Map<String, String> constants = new LinkedHashMap<>();
		for (CatalogRow row : catalog.rows()) {
			keys.add(row.key());
			constants.put(constantName(row.key()), row.key());
		}
		List<Finding> findings = new ArrayList<>();
		for (Path file : javaFiles(sourceRoot)) {
			String relative = sourceRoot.relativize(file).toString().replace('\\', '/');
			if (relative.endsWith(EXEMPT_SUFFIX)) {
				continue;
			}
			String source = read(file);
			JavaLiteralTokenizer.Result tokenized = JavaLiteralTokenizer.tokenize(source);
			String masked = tokenized.masked();
			List<JavaLiteralTokenizer.Token> literals = tokenized.literals();

			for (Match match : matches(PARAMETER_KEYS_CONSTANT, masked)) {
				String constant = match.group();
				if (!constants.containsKey(constant)) {
					findings.add(new Finding(relative, lineOf(masked, match.start()),
							"ParameterKeys." + constant + " is not in the catalog"));
				}
			}
			for (Match match : matches(PARAMETER_KEY_OF, masked)) {
				JavaLiteralTokenizer.Token literal = firstStringLiteral(source, literals, match.end());
				if (literal == null) {
					findings.add(new Finding(relative, lineOf(masked, match.start()),
							"ParameterKey.of first argument is not one string literal"));
				}
				else if (!keys.contains(literal.text())) {
					findings.add(new Finding(relative, literal.line(),
							"ParameterKey.of names " + literal.text() + ", which is not in the catalog"));
				}
			}
			if (STATIC_READER_REFERENCE.matcher(masked).find()) {
				findings.add(new Finding(relative, lineOf(masked, STATIC_READER_REFERENCE.matcher(masked).start()),
						"CatalogParameterReader::get is refused: call get on a declared reader with a literal key"));
			}
			for (Match match : matches(STATIC_READER_GET, masked)) {
				readerCall(relative, source, masked, literals, match.end(), match.start(), keys, findings);
			}
			Set<String> readers = readerNames(masked);
			for (String reader : readers) {
				for (Match ambiguity : matches(
						Pattern.compile("\\b(?!var\\b)(?!this\\b)([A-Z][A-Za-z0-9_]*)\\s+" + Pattern.quote(reader)
								+ "\\s*[;=,)]"),
						masked)) {
					if (!READER.equals(ambiguity.group())) {
						findings.add(new Finding(relative, lineOf(masked, ambiguity.start()),
								reader + " is declared both as a reader and as " + ambiguity.group()));
					}
				}
				if (Pattern.compile("\\bvar\\s+[A-Za-z_][A-Za-z0-9_]*\\s*=\\s*" + Pattern.quote(reader) + "\\s*;")
					.matcher(masked)
					.find()) {
					Matcher varLocal = Pattern
						.compile("\\bvar\\s+[A-Za-z_][A-Za-z0-9_]*\\s*=\\s*" + Pattern.quote(reader) + "\\s*;")
						.matcher(masked);
					varLocal.find();
					findings.add(new Finding(relative, lineOf(masked, varLocal.start()),
							"a var local initialised from " + reader + " is refused: declare the reader type"));
				}
				if (Pattern.compile(Pattern.quote(reader) + "\\s*::\\s*get\\b").matcher(masked).find()) {
					Matcher reference = Pattern.compile(Pattern.quote(reader) + "\\s*::\\s*get\\b").matcher(masked);
					reference.find();
					findings.add(new Finding(relative, lineOf(masked, reference.start()),
							reader + "::get is refused: call get with a literal key"));
				}
				for (Match match : matches(
						Pattern.compile("(?:\\bthis\\s*\\.\\s*)?" + Pattern.quote(reader) + "\\s*\\.\\s*get\\s*\\("),
						masked)) {
					readerCall(relative, source, masked, literals, match.end(), match.start(), keys, findings);
				}
			}
		}
		return List.copyOf(findings);
	}

	/** Rules 2 to 4, re-checked on the parsed rows so a hand-edited file cannot bypass the parser. */
	public static List<Finding> rowRules(CatalogFileParser.Result catalog) {
		List<Finding> findings = new ArrayList<>();
		for (CatalogFileParser.CatalogFinding finding : catalog.findings()) {
			findings.add(new Finding(finding.key(), 0, finding.column() + ": " + finding.message()));
		}
		Set<String> seen = new LinkedHashSet<>();
		for (CatalogRow row : catalog.rows()) {
			if (!seen.add(row.key())) {
				findings.add(new Finding(row.key(), 0, "key: duplicate key"));
			}
			if (row.ownerRole().isBlank() || !row.ownerRole().startsWith("RW-")) {
				findings.add(new Finding(row.key(), 0, "owner_role: an owner is required"));
			}
			if (row.kind().isBlank() || row.scope().isBlank() || row.valueType().isBlank()) {
				findings.add(new Finding(row.key(), 0, "kind: kind, type and scope are required"));
			}
			boolean exempt = "PRODUCT".equals(row.scope()) || row.secret() || "ENV".equals(row.valueSource());
			if (!exempt && row.defaultValue().isBlank()) {
				findings.add(new Finding(row.key(), 0, "default_value: a default is required"));
			}
		}
		return List.copyOf(findings);
	}

	/** Rule 5: the persisted row must equal the catalog row on every mirrored column (TC-27). */
	public static List<Finding> drift(CatalogRow catalogRow, CatalogRow persistedRow) {
		List<Finding> findings = new ArrayList<>();
		diff(findings, catalogRow.key(), "kind", catalogRow.kind(), persistedRow.kind());
		diff(findings, catalogRow.key(), "value_type", catalogRow.valueType(), persistedRow.valueType());
		diff(findings, catalogRow.key(), "unit", catalogRow.unit(), persistedRow.unit());
		diff(findings, catalogRow.key(), "min_value", catalogRow.minValue(), persistedRow.minValue());
		diff(findings, catalogRow.key(), "max_value", catalogRow.maxValue(), persistedRow.maxValue());
		diff(findings, catalogRow.key(), "default_value", catalogRow.defaultValue(), persistedRow.defaultValue());
		diff(findings, catalogRow.key(), "scope", catalogRow.scope(), persistedRow.scope());
		diff(findings, catalogRow.key(), "required", String.valueOf(catalogRow.required()),
				String.valueOf(persistedRow.required()));
		diff(findings, catalogRow.key(), "owner_role", catalogRow.ownerRole(), persistedRow.ownerRole());
		diff(findings, catalogRow.key(), "environments", catalogRow.environmentsText(), persistedRow.environmentsText());
		diff(findings, catalogRow.key(), "used_by", catalogRow.usedByText(), persistedRow.usedByText());
		diff(findings, catalogRow.key(), "secret", String.valueOf(catalogRow.secret()),
				String.valueOf(persistedRow.secret()));
		diff(findings, catalogRow.key(), "description", catalogRow.description(), persistedRow.description());
		return List.copyOf(findings);
	}

	/** The constant name of a catalog key: upper-cased, {@code .} and {@code -} replaced by {@code _}. */
	public static String constantName(String key) {
		return key.toUpperCase(Locale.ROOT).replace('.', '_').replace('-', '_');
	}

	private static void diff(List<Finding> findings, String key, String column, String expected, String actual) {
		if (!expected.equals(actual)) {
			findings.add(new Finding(key, 0, column + ": catalog '" + expected + "' but persisted '" + actual + "'"));
		}
	}

	private static void readerCall(String file, String source, String masked, List<JavaLiteralTokenizer.Token> literals, int from,
			int start, Set<String> keys, List<Finding> findings) {
		JavaLiteralTokenizer.Token literal = firstStringLiteral(source, literals, from);
		if (literal == null) {
			findings.add(new Finding(file, lineOf(masked, start),
					"a reader call's first argument is not one string literal"));
			return;
		}
		if (!keys.contains(literal.text())) {
			findings.add(new Finding(file, literal.line(),
					"reader call names " + literal.text() + ", which is not in the catalog"));
		}
	}

	/** The string literal that starts at {@code from} after whitespace only, or null. */
	private static JavaLiteralTokenizer.Token firstStringLiteral(String source, List<JavaLiteralTokenizer.Token> literals,
			int from) {
		int index = from;
		while (index < source.length() && Character.isWhitespace(source.charAt(index))) {
			index++;
		}
		for (JavaLiteralTokenizer.Token token : literals) {
			if (token.offset() == index) {
				return token.kind() == JavaLiteralTokenizer.Kind.STRING ? token : null;
			}
			if (token.offset() > index) {
				return null;
			}
		}
		return null;
	}

	private static Set<String> readerNames(String masked) {
		Set<String> names = new LinkedHashSet<>();
		Matcher matcher = READER_DECLARATION.matcher(masked);
		while (matcher.find()) {
			String name = matcher.group(1);
			if (!"get".equals(name)) {
				names.add(name);
			}
		}
		return names;
	}

	private record Match(String group, int start, int end) {

		static Match of(Matcher matcher) {
			return new Match(matcher.groupCount() > 0 ? matcher.group(1) : "", matcher.start(), matcher.end());
		}
	}

	private static List<Match> matches(Pattern pattern, String text) {
		List<Match> matches = new ArrayList<>();
		Matcher matcher = pattern.matcher(text);
		while (matcher.find()) {
			matches.add(Match.of(matcher));
		}
		return matches;
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

	private static List<Path> javaFiles(Path root) {
		try (Stream<Path> files = Files.walk(root)) {
			return files.filter(path -> path.toString().endsWith(".java")).sorted().toList();
		}
		catch (IOException ex) {
			throw new UncheckedIOException(ex);
		}
	}

	private static String read(Path file) {
		try {
			return Files.readString(file, StandardCharsets.UTF_8);
		}
		catch (IOException ex) {
			throw new UncheckedIOException(ex);
		}
	}
}
