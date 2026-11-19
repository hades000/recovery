package th.co.scb.ace.demo.recovery.casewf.rules;

import java.util.List;

/**
 * Embedded Drools evaluator (ADR-012). One evaluator serves the engines, the scenarios, the dry
 * run and the build gate, so a scenario that passes proves the production path.
 *
 * <p>From Epic 3, {@link #evaluate} is called only inside a Temporal activity. The caller writes
 * {@link RuleResult#ruleId()} and {@link RuleResult#packageVersion()} to the decision log.
 */
public interface RuleEngine {

	/**
	 * Compiles a Drools XLS/XLSX decision-table workbook. Does not store or activate it; storing a
	 * {@code rule_package_version} row and RW-RISK approval belong to the rule package story (E1-073).
	 *
	 * @throws RuleCompilationException when the workbook does not compile
	 */
	CompiledRulePackage compile(String packageCode, String versionLabel, String fileName, byte[] workbook);

	/**
	 * Evaluates one fact against a compiled package version. First match: exactly one row decides,
	 * or the result is {@link RuleResult#noMatch}.
	 */
	RuleResult evaluate(String packageCode, String versionLabel, RuleInput input);

	/** Thrown when a workbook does not compile. {@code messages} are Drools builder messages. */
	class RuleCompilationException extends RuntimeException {

		private final List<String> messages;

		public RuleCompilationException(String packageCode, List<String> messages) {
			super("Rule package " + packageCode + " does not compile: " + String.join("; ", messages));
			this.messages = List.copyOf(messages);
		}

		public List<String> messages() {
			return messages;
		}
	}
}
