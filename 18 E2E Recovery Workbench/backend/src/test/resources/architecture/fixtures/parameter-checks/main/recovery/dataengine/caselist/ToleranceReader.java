package recovery.dataengine.caselist;

import java.time.LocalDate;
import th.co.scb.ace.demo.recovery.access.api.CatalogParameterReader;

/** Fixture for TC-E1-042-03 (b) to (f) and (h). Not compiled. */
public class ToleranceReader {

	private final CatalogParameterReader tolerances;

	public ToleranceReader(CatalogParameterReader reader) {
		this.tolerances = reader;
	}

	int fromField(LocalDate d) {
		return tolerances.get("allocation.retry.limit", Integer.class, d);
	}

	int fromParameter(LocalDate d) {
		return reader.get("allocation.retry.limit", Integer.class, d);
	}

	int staticForm(LocalDate d) {
		return CatalogParameterReader.get("allocation.retry.limit", Integer.class);
	}

	int nonLiteral(String key, LocalDate d) {
		return tolerances.get(key, Integer.class, d);
	}

	void references() {
		java.util.function.BiFunction<String, Class<?>, Object> f = tolerances::get;
		var r = tolerances;
	}

	int catalogued(LocalDate d) {
		return tolerances.get("config.cache.ttl-seconds", Integer.class, d);
	}
}