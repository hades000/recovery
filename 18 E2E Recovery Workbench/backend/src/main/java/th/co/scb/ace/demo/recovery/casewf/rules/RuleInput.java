package th.co.scb.ace.demo.recovery.casewf.rules;

import java.math.BigDecimal;
import java.util.Map;

/**
 * The fact a decision table matches on. Condition cells read it with {@code num("dpd") >= $param}
 * or {@code text("productGroup") == "$param"}, so a new input needs no code change.
 *
 * <p>Inputs carry business codes and amounts, never a name, ID number or phone number.
 */
public final class RuleInput {

	private final Map<String, Object> values;

	private RuleInput(Map<String, Object> values) {
		this.values = Map.copyOf(values);
	}

	public static RuleInput of(Map<String, Object> values) {
		return new RuleInput(values);
	}

	public BigDecimal num(String key) {
		Object v = values.get(key);
		if (v == null) {
			return null;
		}
		return v instanceof BigDecimal b ? b : new BigDecimal(v.toString());
	}

	public String text(String key) {
		Object v = values.get(key);
		return v == null ? null : v.toString();
	}

	public boolean flag(String key) {
		return Boolean.parseBoolean(text(key));
	}

	public boolean has(String key) {
		return values.containsKey(key);
	}

	public Map<String, Object> values() {
		return values;
	}
}
