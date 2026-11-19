package th.co.scb.ace.demo.recovery.casewf.config.api;

import java.util.List;

/** The catalog metadata of a key; it holds no value (SPEC-RWB-E1-042-017). */
public record CatalogEntry(String key, String kind, String type, String unit, String min, String max,
		String defaultValue, String scope, boolean required, String owner, List<String> environments,
		List<String> usedBy, boolean secret) {

	public CatalogEntry {
		environments = List.copyOf(environments);
		usedBy = List.copyOf(usedBy);
	}
}