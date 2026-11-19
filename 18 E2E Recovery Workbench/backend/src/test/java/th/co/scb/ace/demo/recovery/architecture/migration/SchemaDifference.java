package th.co.scb.ace.demo.recovery.architecture.migration;

/**
 * SPEC-RWB-E1-044-012 (T-044-19, -15): one drift difference. {@code objectPath} is
 * {@code recovery.<table>.<column>}, {@code recovery.<table>.<constraint>}, {@code recovery.<index>}
 * or {@code recovery.<view>}.
 */
public record SchemaDifference(Kind kind, String objectPath) {

	public enum Kind {

		ADDED, MISSING, CHANGED

	}

	public String format() {
		return "MSG-P3-016 schema=recovery object=" + objectPath;
	}

}
