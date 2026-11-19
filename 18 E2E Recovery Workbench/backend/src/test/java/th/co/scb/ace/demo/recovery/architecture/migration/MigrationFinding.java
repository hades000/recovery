package th.co.scb.ace.demo.recovery.architecture.migration;

import java.util.Objects;

/**
 * SPEC-RWB-E1-044-004: one lint finding, rendered as one {@code MSG-P3-016} line.
 *
 * <p>Finding multiplicity: the identity is (rule, file, line, key). Two matches of the same rule
 * with the same identity are one finding, however many positions or items of the rule matched.
 */
public record MigrationFinding(String ruleId, String file, int line, String key, String detail) {

	public String format() {
		String object = file + ":" + line;
		String suffix = (detail == null || detail.isBlank()) ? "" : " " + detail;
		return "MSG-P3-016 schema=recovery object=" + object + " rule=" + ruleId + suffix;
	}

	@Override
	public boolean equals(Object other) {
		if (this == other) {
			return true;
		}
		return other instanceof MigrationFinding that && ruleId.equals(that.ruleId) && file.equals(that.file)
				&& line == that.line && Objects.equals(key, that.key);
	}

	@Override
	public int hashCode() {
		return Objects.hash(ruleId, file, line, key);
	}

	@Override
	public String toString() {
		return format();
	}
}
