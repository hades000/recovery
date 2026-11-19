package th.co.scb.ace.demo.recovery.casewf.rules;

import java.util.LinkedHashMap;
import java.util.Map;

/**
 * Collector bound as the decision-table global {@code outcome} (declared in the workbook's
 * {@code Variables} row as {@code RuleOutcome outcome}). An action cell calls
 * {@code outcome.decide(drools.getRule().getName())} and then {@code outcome.put("targetQueue", "$param")}.
 */
public final class RuleOutcome {

	private String ruleId;
	private final Map<String, String> outputs = new LinkedHashMap<>();

	public void decide(String ruleId) {
		if (this.ruleId != null && !this.ruleId.equals(ruleId)) {
			throw new IllegalStateException("Two rows decided: " + this.ruleId + " and " + ruleId);
		}
		this.ruleId = ruleId;
	}

	public void put(String key, String value) {
		outputs.put(key, value);
	}

	public String ruleId() {
		return ruleId;
	}

	public Map<String, String> outputs() {
		return Map.copyOf(outputs);
	}
}
