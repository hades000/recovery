package th.co.scb.ace.demo.recovery.casewf.config;

import java.time.LocalDate;
import java.util.List;

import com.fasterxml.jackson.annotation.JsonInclude;
import com.fasterxml.jackson.annotation.JsonProperty;

/**
 * One element of the {@code GET /admin/parameters} answer; its JSON matches API Specification v4
 * {@code Parameter} (SPEC-RWB-E1-042-011). An absent value, default or version is left out rather
 * than sent as null, so a secret has no value and no default and a PRODUCT row has no value.
 */
@JsonInclude(JsonInclude.Include.NON_NULL)
record CatalogParameterView(String key, String kind, String type, String unit, String min, String max,
		@JsonProperty("default") String defaultValue, String scope, boolean required, String owner,
		List<String> environments, List<String> usedBy, boolean secret, String valueInForce, Integer versionNo,
		LocalDate validFrom) {
}