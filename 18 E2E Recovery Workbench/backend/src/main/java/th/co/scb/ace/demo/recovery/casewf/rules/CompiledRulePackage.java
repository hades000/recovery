package th.co.scb.ace.demo.recovery.casewf.rules;

import java.util.List;

/**
 * Result of compiling a workbook: the generated DRL and its checksum, stored with the workbook on
 * the {@code rule_package_version} row (ADR-012).
 *
 * @param ruleIds rule names in the package, in row order; the default row is last
 */
public record CompiledRulePackage(String packageCode, String versionLabel, String drlSource, String drlSha256,
		List<String> ruleIds) {
}
