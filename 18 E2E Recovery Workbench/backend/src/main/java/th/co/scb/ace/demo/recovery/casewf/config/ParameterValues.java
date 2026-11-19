package th.co.scb.ace.demo.recovery.casewf.config;

import java.math.BigDecimal;
import java.time.Duration;
import java.time.LocalDate;
import java.time.LocalTime;
import java.util.ArrayList;
import java.util.List;

import th.co.scb.ace.demo.recovery.casewf.config.api.ParameterKey;

/**
 * The one converter from catalog text to a typed value (SPEC-RWB-E1-042-005). {@code
 * ParameterServiceImpl}, {@code ParameterLoadValidator} and {@code ParameterStartupCheck} all call
 * it, so the load check and the read path cannot disagree about a value.
 */
final class ParameterValues {

	private ParameterValues() {
	}

	@SuppressWarnings("unchecked")
	static <T> T convert(ParameterKey<T> key, String text) {
		if (text == null) {
			throw new IllegalArgumentException(key.name());
		}
		Object value = switch (key.type().getName()) {
			case "java.lang.Integer" -> Integer.valueOf(text);
			case "java.math.BigDecimal" -> new BigDecimal(text);
			case "java.lang.Boolean" -> booleanValue(key, text);
			case "java.time.LocalDate" -> LocalDate.parse(text);
			case "java.time.LocalTime" -> LocalTime.parse(text);
			case "java.time.Duration" -> Duration.parse(text);
			case "java.util.List" -> codeList(text);
			default -> text;
		};
		return (T) value;
	}

	/** Whether the text converts; used by the load check, which must refuse rather than throw. */
	static boolean converts(ParameterKey<?> key, String text) {
		try {
			convert(key, text);
			return true;
		}
		catch (RuntimeException ex) {
			return false;
		}
	}

	private static Boolean booleanValue(ParameterKey<?> key, String text) {
		if ("true".equals(text)) {
			return Boolean.TRUE;
		}
		if ("false".equals(text)) {
			return Boolean.FALSE;
		}
		throw new IllegalArgumentException(key.name());
	}

	private static List<String> codeList(String text) {
		List<String> values = new ArrayList<>();
		for (String part : text.split(",", -1)) {
			String value = part.trim();
			if (!value.isEmpty()) {
				values.add(value);
			}
		}
		return List.copyOf(values);
	}
}
