package th.co.scb.ace.demo.recovery.casewf.rules;

import java.util.Map;

/**
 * Evaluation result. {@code ruleId} is the Drools rule name and {@code packageVersion} the package
 * version label; both go to {@code decision_log_entry.rule_id} and {@code rule_version} (ADR-012).
 */
public record RuleResult(String packageCode, String packageVersion, String ruleId, Map<String, String> outputs) {

	public static RuleResult noMatch(String packageCode, String packageVersion) {
		return new RuleResult(packageCode, packageVersion, null, Map.of());
	}

	public boolean matched() {
		return ruleId != null;
	}
}
