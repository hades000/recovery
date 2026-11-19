package th.co.scb.ace.demo.recovery.casewf.config.api;

import java.util.List;
import java.util.Objects;

/**
 * A typed handle on one catalog parameter (SPEC-RWB-E1-042-005). Every instance carries the
 * catalog's metadata, so a caller that holds a key needs no second lookup and no business value is
 * ever written in code. Production code uses the generated constants in {@link ParameterKeys};
 * {@link #of(String, Class)} exists for fixture modules and for the completeness check.
 *
 * <p>The metadata accessors that name a catalog token ({@code kind}, {@code scope},
 * {@code valueSource}) return the token as written, so the published surface stays the eleven types
 * of the spec instead of adding nested enums to {@code casewf.config.api}.
 *
 * @param <T> the Java type the catalog's {@code value_type} maps to
 */
public final class ParameterKey<T> {

	private final String name;

	private final Class<T> type;

	private final String kind;

	private final String unit;

	private final String min;

	private final String max;

	private final String defaultValue;

	private final String scope;

	private final boolean required;

	private final String ownerRole;

	private final List<String> environments;

	private final List<String> usedBy;

	private final boolean secret;

	private final String valueSource;

	private final String envProperty;

	private final String description;

	public ParameterKey(String name, Class<T> type, String kind, String unit, String min, String max,
			String defaultValue, String scope, boolean required, String ownerRole, List<String> environments,
			List<String> usedBy, boolean secret, String valueSource, String envProperty, String description) {
		this.name = Objects.requireNonNull(name, "name");
		this.type = Objects.requireNonNull(type, "type");
		this.kind = orEmpty(kind);
		this.unit = orEmpty(unit);
		this.min = orEmpty(min);
		this.max = orEmpty(max);
		this.defaultValue = defaultValue == null || defaultValue.isEmpty() ? null : defaultValue;
		this.scope = orEmpty(scope);
		this.required = required;
		this.ownerRole = orEmpty(ownerRole);
		this.environments = List.copyOf(environments == null ? List.of() : environments);
		this.usedBy = List.copyOf(usedBy == null ? List.of() : usedBy);
		this.secret = secret;
		this.valueSource = orEmpty(valueSource);
		this.envProperty = envProperty == null || envProperty.isEmpty() ? null : envProperty;
		this.description = orEmpty(description);
	}

	/** An ad-hoc key with no catalog metadata, for fixtures and the completeness check. */
	public static <T> ParameterKey<T> of(String name, Class<T> type) {
		return new ParameterKey<>(name, type, "", "", "", "", null, "GLOBAL", false, "", List.of(), List.of(), false,
				"", null, "");
	}

	public String name() {
		return name;
	}

	public Class<T> type() {
		return type;
	}

	public String kind() {
		return kind;
	}

	public String unit() {
		return unit;
	}

	public String min() {
		return min;
	}

	public String max() {
		return max;
	}

	public String defaultValue() {
		return defaultValue;
	}

	public String scope() {
		return scope;
	}

	public boolean required() {
		return required;
	}

	public String ownerRole() {
		return ownerRole;
	}

	public List<String> environments() {
		return environments;
	}

	public List<String> usedBy() {
		return usedBy;
	}

	public boolean secret() {
		return secret;
	}

	public String valueSource() {
		return valueSource;
	}

	public String envProperty() {
		return envProperty;
	}

	public String description() {
		return description;
	}

	@Override
	public boolean equals(Object other) {
		return other instanceof ParameterKey<?> candidate && name.equals(candidate.name) && type.equals(candidate.type);
	}

	@Override
	public int hashCode() {
		return Objects.hash(name, type);
	}

	@Override
	public String toString() {
		return name;
	}

	private static String orEmpty(String value) {
		return value == null ? "" : value;
	}
}
