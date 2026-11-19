package th.co.scb.ace.demo.recovery.casewf.config;

import java.nio.ByteBuffer;
import java.nio.charset.CharacterCodingException;
import java.nio.charset.CodingErrorAction;
import java.nio.charset.StandardCharsets;
import java.time.LocalDate;
import java.util.ArrayList;
import java.util.LinkedHashSet;
import java.util.List;
import java.util.Map;
import java.util.Set;

import org.springframework.http.HttpStatus;
import org.springframework.stereotype.Component;

import th.co.scb.ace.demo.recovery.access.api.ApiProblemException;
import th.co.scb.ace.demo.recovery.casewf.config.api.ParameterKey;
import th.co.scb.ace.demo.recovery.casewf.config.api.ParameterLoadHandler;
import th.co.scb.ace.demo.recovery.casewf.config.api.ParameterKeys;

/**
 * The twelve checks of SPEC-RWB-E1-042-012, in the order of §12.5; the first failure refuses the
 * whole load and nothing is written. Every refusal is an {@code access.api.ApiProblemException} with
 * its message ID, placeholders and, where it applies, the failing field. The identical-repeat check
 * (11) is the handler's, because it needs the content hash.
 */
@Component
class ParameterLoadValidator {

	static final String HEADER = "key,environment,value";

	private final ParameterValueRepository values;

	ParameterLoadValidator(ParameterValueRepository values) {
		this.values = values;
	}

	List<ParameterContentHash.Row> validate(byte[] content, LocalDate validFrom, LocalDate businessDate) {
		// 1. file content and validFrom present.
		if (content == null || content.length == 0) {
			throw missing("file");
		}
		if (validFrom == null) {
			throw missing("validFrom");
		}
		// 2. a CSV with the exact header and at least one row.
		List<CsvRows.Row> rows;
		try {
			rows = CsvRows.parse(decode(content, validFrom));
		}
		catch (CsvRows.CsvFormatException ex) {
			throw check(validFrom, "file is not a CSV with header " + HEADER);
		}
		if (rows.isEmpty() || !HEADER.equals(String.join(",", rows.get(0).fields()))) {
			throw check(validFrom, "file is not a CSV with header " + HEADER);
		}
		List<CsvRows.Row> data = rows.subList(1, rows.size());
		if (data.isEmpty()) {
			throw missing("file");
		}
		// 3. validFrom is not before the business date.
		if (validFrom.isBefore(businessDate)) {
			throw new ApiProblemException(HttpStatus.UNPROCESSABLE_ENTITY, "MSG-P3-027",
					Map.of("table", ParameterLoadHandler.TABLE, "check", "valid from is before the business date"), null,
					null, null);
		}
		List<ParameterContentHash.Row> loaded = new ArrayList<>();
		Set<String> seen = new LinkedHashSet<>();
		for (CsvRows.Row row : data) {
			String key = row.field(0).trim();
			String environment = row.field(1).trim();
			String value = row.field(2);
			// 4. the key is in the catalog.
			ParameterKey<?> definition = ParameterKeys.all()
				.stream()
				.filter(candidate -> candidate.name().equals(key))
				.findFirst()
				.orElseThrow(() -> check(validFrom, "key " + key + " is not in the catalog"));
			// 5. the key is loadable: not secret, not PRODUCT, not ENV.
			if (definition.secret() || "PRODUCT".equals(definition.scope()) || "ENV".equals(definition.valueSource())) {
				throw check(validFrom, "key " + key + " cannot be loaded as a value");
			}
			// 6. the environment is listed for the key.
			if (!definition.environments().contains(environment)) {
				throw check(validFrom, "environment " + environment + " is not listed for " + key);
			}
			// 7. the value is not blank and fits the column.
			if (value.trim().isEmpty()) {
				throw missing("value of " + key);
			}
			if (value.trim().length() > ParameterSchemaLimits.PARAM_VALUE_MAX) {
				throw check(validFrom, "value is longer than " + ParameterSchemaLimits.PARAM_VALUE_MAX + " characters");
			}
			// 8. the value parses as the type.
			if (!ParameterValues.converts(definition, value.trim())) {
				throw check(validFrom, "value is not " + ParameterServiceImpl.typeName(definition.type()));
			}
			// 9. the value is within min..max.
			withinRange(definition, value.trim());
			// 10. no duplicate (key, environment) in the file.
			if (!seen.add(key + "|" + environment)) {
				throw check(validFrom, "duplicate row for " + key + " " + environment);
			}
			loaded.add(new ParameterContentHash.Row(key, environment, value.trim()));
		}
		return List.copyOf(loaded);
	}

	/**
	 * Check 12 of §12.5: no approved row of (key, environment) starts on or after this load's date.
	 * It runs **after** the identical-repeat lookup (check 11), because the load's own approved rows
	 * would otherwise refuse its own repeat (code-gate CODE-001).
	 */
	void validateApprovalWindow(List<ParameterContentHash.Row> loaded, LocalDate validFrom) {
		for (ParameterContentHash.Row row : loaded) {
			if (values.countApprovedFrom(row.key(), row.environment(), validFrom) > 0) {
				throw new ApiProblemException(HttpStatus.CONFLICT, "MSG-P3-027",
						Map.of("table", ParameterLoadHandler.TABLE, "check",
								"an approved version from " + validFrom + " exists for " + row.key() + " "
										+ row.environment()),
						null, null, null);
			}
		}
	}

	/** Strict UTF-8: a malformed byte is a refusal, never a replacement character (review Should 8). */
	private static String decode(byte[] content, LocalDate validFrom) {
		try {
			return StandardCharsets.UTF_8.newDecoder()
				.onMalformedInput(CodingErrorAction.REPORT)
				.onUnmappableCharacter(CodingErrorAction.REPORT)
				.decode(ByteBuffer.wrap(content))
				.toString();
		}
		catch (CharacterCodingException ex) {
			throw check(validFrom, "file is not UTF-8");
		}
	}

	/** The rollback reason: non-blank and at most the schema width after trim (SPEC-RWB-E1-042-015). */
	static String validateReason(String reason) {
		String trimmed = reason == null ? "" : reason.trim();
		if (trimmed.isEmpty() || trimmed.length() > ParameterSchemaLimits.ROLLBACK_REASON_MAX) {
			throw missing("reason");
		}
		return trimmed;
	}

	@SuppressWarnings({ "unchecked", "rawtypes" })
	private static void withinRange(ParameterKey<?> definition, String value) {
		if (definition.min().isEmpty() && definition.max().isEmpty()) {
			return;
		}
		Comparable actual = (Comparable) ParameterValues.convert(cast(definition), value);
		if (!definition.min().isEmpty() && actual.compareTo(ParameterValues.convert(cast(definition),
				definition.min())) < 0) {
			throw outOfRange(definition);
		}
		if (!definition.max().isEmpty() && actual.compareTo(ParameterValues.convert(cast(definition),
				definition.max())) > 0) {
			throw outOfRange(definition);
		}
	}

	private static ApiProblemException outOfRange(ParameterKey<?> definition) {
		return new ApiProblemException(HttpStatus.UNPROCESSABLE_ENTITY, "MSG-GEN-002",
				Map.of("field", definition.name(), "min", definition.min(), "max", definition.max()), definition.name(),
				null, null);
	}

	@SuppressWarnings("unchecked")
	private static <T> ParameterKey<T> cast(ParameterKey<?> key) {
		return (ParameterKey<T>) key;
	}

	private static ApiProblemException missing(String field) {
		return new ApiProblemException(HttpStatus.UNPROCESSABLE_ENTITY, "MSG-GEN-001", Map.of("field", field), field,
				null, null);
	}

	private static ApiProblemException check(LocalDate validFrom, String check) {
		return new ApiProblemException(HttpStatus.UNPROCESSABLE_ENTITY, "MSG-P1-002",
				Map.of("source", ParameterLoadHandler.TABLE, "date", validFrom == null ? "" : validFrom.toString(),
						"check", check),
				null, null, null);
	}
}
