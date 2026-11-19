package th.co.scb.ace.demo.recovery.architecture.parameters;

import java.util.List;

/**
 * One parsed row of the parameter catalog (SPEC-RWB-E1-042-003, -005). It mirrors the catalog file
 * column for column; {@code environmentsText} and {@code usedByText} keep the cell as written so
 * the database copy can be compared with it.
 */
public record CatalogRow(String key, String kind, String valueType, String unit, String minValue, String maxValue,
		String defaultValue, String scope, boolean required, String ownerRole, String environmentsText,
		List<String> environments, String usedByText, List<String> usedBy, boolean secret, String valueSource,
		String envProperty, String description) {

	public CatalogRow {
		environments = List.copyOf(environments);
		usedBy = List.copyOf(usedBy);
	}
}
