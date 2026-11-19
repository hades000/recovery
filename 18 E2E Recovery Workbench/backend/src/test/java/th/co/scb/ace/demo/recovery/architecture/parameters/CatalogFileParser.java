package th.co.scb.ace.demo.recovery.architecture.parameters;

import java.io.IOException;
import java.io.UncheckedIOException;
import java.math.BigDecimal;
import java.nio.charset.StandardCharsets;
import java.nio.file.Files;
import java.nio.file.Path;
import java.time.Duration;
import java.time.LocalDate;
import java.time.LocalTime;
import java.util.ArrayList;
import java.util.LinkedHashMap;
import java.util.List;
import java.util.Locale;
import java.util.Map;
import java.util.Set;
import java.util.regex.Pattern;

import th.co.scb.ace.demo.recovery.casewf.config.CsvRows;

/**
 * The catalog-file rules of SPEC-RWB-E1-042-003 and §7.1 of the spec. Header, key, kind, type, unit,
 * range, default, scope, required, owner, environments, the {@code used_by} grammar, the secret
 * rules, {@code value_source}, the credential-name rule on {@code env_property} and the description
 * length are checked here so the file, the generated keys and the database copy cannot disagree.
 */
public final class CatalogFileParser {

	public static final String HEADER = "key,kind,value_type,unit,min_value,max_value,default_value,scope,required,"
			+ "owner_role,environments,used_by,secret,value_source,env_property,description";

	static final Set<String> KINDS = Set.of("BUSINESS", "ENVIRONMENT");

	static final Set<String> VALUE_TYPES = Set.of("STRING", "INTEGER", "DECIMAL", "BOOLEAN", "DATE", "TIME", "DURATION",
			"CODE", "CODE_LIST", "JSON");

	static final Set<String> SCOPES = Set.of("GLOBAL", "PRODUCT");

	static final Set<String> VALUE_SOURCES = Set.of("TABLE", "ENV", "SECRET");

	static final Set<String> ENVIRONMENTS = Set.of("DEV", "SIT", "UAT", "PROD");

	/**
	 * The credential-name rule of §7.1 and finding 138, widened by security review SEC-042-03: a
	 * connection string carries {@code AccountKey=}, and {@code pwd} is the short form of a password.
	 */
	static final List<String> CREDENTIAL_WORDS = List.of("password", "passwd", "pwd", "secret", "token",
			"credential", "apikey", "api-key", "api_key", "privatekey", "private-key", "private_key",
			"connection-string", "connectionstring", "accountkey", "passphrase", "sas-token");

	static final int KEY_MAX = 100;

	static final int UNIT_MAX = 20;

	static final int OWNER_MAX = 20;

	static final int ENVIRONMENTS_MAX = 40;

	static final int USED_BY_ENTRY_MAX = 100;

	static final int USED_BY_TOTAL_MAX = 400;

	static final int DESCRIPTION_MAX = 400;

	private static final Pattern KEY = Pattern.compile("^[A-Za-z][A-Za-z0-9_.-]{0,99}$");

	/** One refusal: the row's key (empty for a file-level finding), the column and the reason. */
	public record CatalogFinding(String key, String column, String message) {

		@Override
		public String toString() {
			return key + "/" + column + ": " + message;
		}
	}

	/** The rows that passed every rule and every finding. */
	public record Result(List<CatalogRow> rows, List<CatalogFinding> findings) {

		public Result {
			rows = List.copyOf(rows);
			findings = List.copyOf(findings);
		}
	}

	private CatalogFileParser() {
	}

	public static Result parse(Path file) {
		try {
			return parse(Files.readString(file, StandardCharsets.UTF_8));
		}
		catch (IOException ex) {
			throw new UncheckedIOException("cannot read " + file, ex);
		}
	}

	public static Result parse(String text) {
		List<CatalogFinding> findings = new ArrayList<>();
		List<CatalogRow> rows = new ArrayList<>();
		List<CsvRows.Row> parsed;
		try {
			parsed = CsvRows.parse(text);
		}
		catch (CsvRows.CsvFormatException ex) {
			findings.add(new CatalogFinding("", "header", "file is not a CSV: " + ex.getMessage()));
			return new Result(rows, findings);
		}
		if (parsed.isEmpty()) {
			findings.add(new CatalogFinding("", "header", "the catalog file is empty"));
			return new Result(rows, findings);
		}
		if (!HEADER.equals(String.join(",", parsed.get(0).fields()))) {
			findings.add(new CatalogFinding("", "header", "the header is not the sixteen columns of §7.1"));
			return new Result(rows, findings);
		}
		Map<String, Integer> seen = new LinkedHashMap<>();
		for (CsvRows.Row row : parsed.subList(1, parsed.size())) {
			List<CatalogFinding> rowFindings = new ArrayList<>();
			CatalogRow catalogRow = row(row, rowFindings);
			String key = row.field(0).trim();
			if (!key.isEmpty()) {
				if (seen.containsKey(key)) {
					rowFindings.add(new CatalogFinding(key, "key", "duplicate key"));
				}
				seen.put(key, row.line());
			}
			findings.addAll(rowFindings);
			if (rowFindings.isEmpty() && catalogRow != null) {
				rows.add(catalogRow);
			}
		}
		return new Result(rows, findings);
	}

	private static CatalogRow row(CsvRows.Row row, List<CatalogFinding> findings) {
		if (row.fields().size() != 16) {
			findings.add(new CatalogFinding(row.field(0), "header", "row has " + row.fields().size() + " columns, not 16"));
			return null;
		}
		String key = row.field(0).trim();
		String kind = row.field(1).trim();
		String valueType = row.field(2).trim();
		String unit = row.field(3).trim();
		String minValue = row.field(4).trim();
		String maxValue = row.field(5).trim();
		String defaultValue = row.field(6).trim();
		String scope = row.field(7).trim();
		String required = row.field(8).trim();
		String ownerRole = row.field(9).trim();
		String environmentsText = row.field(10).trim();
		String usedByText = row.field(11);
		String secret = row.field(12).trim();
		String valueSource = row.field(13).trim();
		String envProperty = row.field(14).trim();
		String description = row.field(15);

		if (!KEY.matcher(key).matches() || key.length() > KEY_MAX) {
			findings.add(new CatalogFinding(key, "key", "key must match " + KEY.pattern()));
		}
		if (!KINDS.contains(kind)) {
			findings.add(new CatalogFinding(key, "kind", "kind must be BUSINESS or ENVIRONMENT"));
		}
		if (!VALUE_TYPES.contains(valueType)) {
			findings.add(new CatalogFinding(key, "value_type", "value_type is not one of the ten types"));
		}
		if (unit.length() > UNIT_MAX) {
			findings.add(new CatalogFinding(key, "unit", "unit is longer than " + UNIT_MAX));
		}
		if (!SCOPES.contains(scope)) {
			findings.add(new CatalogFinding(key, "scope", "scope must be GLOBAL or PRODUCT"));
		}
		if (!"true".equals(required) && !"false".equals(required)) {
			findings.add(new CatalogFinding(key, "required", "required must be true or false"));
		}
		if (!ownerRole.startsWith("RW-") || ownerRole.length() > OWNER_MAX) {
			findings.add(new CatalogFinding(key, "owner_role", "owner_role must be an RW- role code"));
		}
		List<String> environments = environments(key, environmentsText, findings);
		List<String> usedBy = usedBy(key, usedByText, findings);
		if (!"true".equals(secret) && !"false".equals(secret)) {
			findings.add(new CatalogFinding(key, "secret", "secret must be true or false"));
		}
		if (!VALUE_SOURCES.contains(valueSource)) {
			findings.add(new CatalogFinding(key, "value_source", "value_source must be TABLE, ENV or SECRET"));
		}
		boolean isSecret = "true".equals(secret);
		if (isSecret && !"SECRET".equals(valueSource)) {
			findings.add(new CatalogFinding(key, "secret", "a secret row must have value_source SECRET"));
		}
		if (isSecret && !defaultValue.isEmpty()) {
			findings.add(new CatalogFinding(key, "secret", "a secret row must have an empty default"));
			findings.add(new CatalogFinding(key, "default_value", "a secret row must have an empty default"));
		}
		if ("ENV".equals(valueSource)) {
			if (envProperty.isEmpty()) {
				findings.add(new CatalogFinding(key, "env_property", "an ENV row needs env_property"));
			}
			else if (namesACredential(envProperty)) {
				findings.add(new CatalogFinding(key, "env_property",
						"env_property names a credential-bearing property; such a value is secret"));
			}
		}
		else if (!envProperty.isEmpty()) {
			findings.add(new CatalogFinding(key, "env_property", "env_property is only for value_source ENV"));
		}
		checkRange(key, valueType, minValue, maxValue, findings);
		checkDefault(key, valueType, defaultValue, minValue, maxValue, scope, isSecret, valueSource, findings);
		if (description.isBlank()) {
			findings.add(new CatalogFinding(key, "description", "description is required"));
		}
		else if (description.length() > DESCRIPTION_MAX) {
			findings.add(new CatalogFinding(key, "description", "description is longer than " + DESCRIPTION_MAX));
		}
		if (!findings.isEmpty()) {
			return null;
		}
		return new CatalogRow(key, kind, valueType, unit, minValue, maxValue, defaultValue, scope,
				Boolean.parseBoolean(required), ownerRole, environmentsText, environments, usedByText, usedBy, isSecret,
				valueSource, envProperty, description);
	}

	private static List<String> environments(String key, String text, List<CatalogFinding> findings) {
		if (text.isEmpty() || text.length() > ENVIRONMENTS_MAX) {
			findings.add(new CatalogFinding(key, "environments", "environments must be a comma list of DEV, SIT, UAT, PROD"));
			return List.of();
		}
		List<String> parsed = new ArrayList<>();
		for (String part : text.split(",", -1)) {
			String value = part.trim();
			if (!ENVIRONMENTS.contains(value)) {
				findings.add(new CatalogFinding(key, "environments", "unknown environment " + value));
				return List.of();
			}
			parsed.add(value);
		}
		return List.copyOf(parsed);
	}

	/** The {@code used_by} grammar of §7.1 (finding 130): one or more {@code ;}-separated entries. */
	private static List<String> usedBy(String key, String text, List<CatalogFinding> findings) {
		if (text.isBlank()) {
			findings.add(new CatalogFinding(key, "used_by", "used_by is required"));
			return List.of();
		}
		if (text.length() > USED_BY_TOTAL_MAX) {
			findings.add(new CatalogFinding(key, "used_by", "used_by is longer than " + USED_BY_TOTAL_MAX));
			return List.of();
		}
		List<String> parsed = new ArrayList<>();
		for (String part : text.split(";", -1)) {
			String entry = part.trim();
			if (entry.isEmpty()) {
				findings.add(new CatalogFinding(key, "used_by", "an entry is empty"));
				return List.of();
			}
			if (entry.length() > USED_BY_ENTRY_MAX) {
				findings.add(new CatalogFinding(key, "used_by", "an entry is longer than " + USED_BY_ENTRY_MAX));
				return List.of();
			}
			if (entry.indexOf('\n') >= 0 || entry.indexOf('\r') >= 0) {
				findings.add(new CatalogFinding(key, "used_by", "an entry holds a line break"));
				return List.of();
			}
			if (entry.indexOf(';') >= 0) {
				findings.add(new CatalogFinding(key, "used_by", "an entry holds a semicolon"));
				return List.of();
			}
			parsed.add(entry);
		}
		return List.copyOf(parsed);
	}

	/** The credential-name rule of §7.1 and finding 138: split on {@code .} only. */
	static boolean namesACredential(String property) {
		for (String segment : property.split("\\.", -1)) {
			String lower = segment.toLowerCase(Locale.ROOT);
			for (String word : CREDENTIAL_WORDS) {
				if (lower.contains(word)) {
					return true;
				}
			}
		}
		return false;
	}

	private static void checkRange(String key, String valueType, String minValue, String maxValue,
			List<CatalogFinding> findings) {
		Object min = parse(valueType, minValue, key, "min_value", findings);
		Object max = parse(valueType, maxValue, key, "max_value", findings);
		if (min != null && max != null && compare(min, max) > 0) {
			findings.add(new CatalogFinding(key, "min_value", "min_value is greater than max_value"));
		}
	}

	private static void checkDefault(String key, String valueType, String defaultValue, String minValue,
			String maxValue, String scope, boolean secret, String valueSource, List<CatalogFinding> findings) {
		boolean exempt = "PRODUCT".equals(scope) || secret || "ENV".equals(valueSource);
		if (defaultValue.isEmpty()) {
			if (!exempt) {
				findings.add(new CatalogFinding(key, "default_value",
						"default_value is required unless the row is PRODUCT, secret or ENV"));
			}
			return;
		}
		Object parsed = parse(valueType, defaultValue, key, "default_value", findings);
		if (parsed == null) {
			return;
		}
		Object min = optionalConvert(valueType, minValue);
		Object max = optionalConvert(valueType, maxValue);
		if (min != null && compare(parsed, min) < 0 || max != null && compare(parsed, max) > 0) {
			findings.add(new CatalogFinding(key, "default_value", "default_value is outside min_value..max_value"));
		}
	}

	private static Object optionalConvert(String valueType, String text) {
		if (text.isEmpty()) {
			return null;
		}
		try {
			return convert(valueType, text);
		}
		catch (RuntimeException ex) {
			return null;
		}
	}

	private static Object parse(String valueType, String text, String key, String column,
			List<CatalogFinding> findings) {
		if (text.isEmpty()) {
			return null;
		}
		try {
			return convert(valueType, text);
		}
		catch (RuntimeException ex) {
			findings.add(new CatalogFinding(key, column, "does not parse as " + valueType));
			return null;
		}
	}

	private static Object convert(String valueType, String text) {
		return switch (valueType) {
			case "INTEGER" -> Integer.valueOf(text);
			case "DECIMAL" -> new BigDecimal(text);
			case "BOOLEAN" -> {
				if (!"true".equals(text) && !"false".equals(text)) {
					throw new IllegalArgumentException("not a boolean");
				}
				yield Boolean.valueOf(text);
			}
			case "DATE" -> LocalDate.parse(text);
			case "TIME" -> LocalTime.parse(text);
			case "DURATION" -> Duration.parse(text);
			default -> text;
		};
	}

	@SuppressWarnings({ "unchecked", "rawtypes" })
	private static int compare(Object left, Object right) {
		if (left instanceof BigDecimal decimal) {
			return decimal.compareTo((BigDecimal) right);
		}
		return ((Comparable) left).compareTo(right);
	}
}
