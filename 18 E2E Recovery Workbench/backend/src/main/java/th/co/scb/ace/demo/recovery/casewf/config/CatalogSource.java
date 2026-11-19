package th.co.scb.ace.demo.recovery.casewf.config;

import java.util.List;
import java.util.Optional;

import org.springframework.stereotype.Component;

import th.co.scb.ace.demo.recovery.casewf.config.api.ParameterKey;
import th.co.scb.ace.demo.recovery.casewf.config.api.ParameterKeys;

/**
 * The catalog metadata a component reads (SPEC-RWB-E1-042-005, -016). Production returns the
 * generated keys; a test replaces the bean to supply a catalog with one default removed.
 */
@Component
class CatalogSource {

	List<ParameterKey<?>> all() {
		return ParameterKeys.all();
	}

	Optional<ParameterKey<?>> byName(String key) {
		return ParameterKeys.all().stream().filter(candidate -> candidate.name().equals(key)).findFirst();
	}
}
