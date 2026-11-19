package th.co.scb.ace.demo.recovery.casewf.config;

import java.time.LocalDate;
import java.util.List;
import java.util.Objects;
import java.util.Optional;

import org.springframework.beans.factory.annotation.Value;
import org.springframework.core.env.Environment;
import org.springframework.stereotype.Service;

import th.co.scb.ace.demo.recovery.casewf.config.api.CatalogEntry;
import th.co.scb.ace.demo.recovery.casewf.config.api.ParameterKey;
import th.co.scb.ace.demo.recovery.casewf.config.api.ParameterNotInForceException;
import th.co.scb.ace.demo.recovery.casewf.config.api.ParameterService;
import th.co.scb.ace.demo.recovery.casewf.config.api.ParameterValue;
import th.co.scb.ace.demo.recovery.casewf.config.api.SecretNotServedException;

/**
 * Resolution of a catalog parameter (SPEC-RWB-E1-042-007, -008, -010, -022, -023, -024). Order: a
 * secret is refused; a PRODUCT key is refused (RWB-E1-045 owns its values); an ENV key resolves the
 * Spring property; a TABLE key takes the approved row in force on the business date, else its catalog
 * default with {@code versionNo 0}. With {@code rwb.p3.configservice} off no database read happens and
 * only defaults and ENV values are served.
 */
@Service
class ParameterServiceImpl implements ParameterService {

	private final ParameterCache cache;

	private final CatalogSource catalog;

	private final Environment environment;

	private final boolean enabled;

	private final String runningEnvironment;

	ParameterServiceImpl(ParameterCache cache, CatalogSource catalog, Environment environment,
			@Value("${rwb.p3.configservice:false}") boolean enabled,
			@Value("${rwb.environment}") String runningEnvironment) {
		this.cache = cache;
		this.catalog = catalog;
		this.environment = environment;
		this.enabled = enabled;
		this.runningEnvironment = runningEnvironment;
	}

	@Override
	public <T> ParameterValue<T> get(ParameterKey<T> key, LocalDate businessDate) {
		return resolve(key, null, businessDate);
	}

	@Override
	public <T> ParameterValue<T> get(ParameterKey<T> key, String productGroup, LocalDate businessDate) {
		return resolve(key, productGroup, businessDate);
	}

	@Override
	public CatalogEntry entry(String key) {
		ParameterKey<?> definition = catalog.byName(key)
			.orElseThrow(() -> new IllegalArgumentException("unknown parameter " + key));
		return new CatalogEntry(definition.name(), definition.kind(), typeName(definition.type()), definition.unit(),
				definition.min(), definition.max(), definition.defaultValue(), definition.scope(),
				definition.required(), definition.ownerRole(), definition.environments(), definition.usedBy(),
				definition.secret());
	}

	/** The value in force for a requested environment; null when the catalog has none to give (SPEC-011). */
	ParameterValue<?> inEnvironment(ParameterKey<?> key, String environmentName, LocalDate businessDate) {
		if (key.secret() || "PRODUCT".equals(key.scope())) {
			return null;
		}
		if ("ENV".equals(key.valueSource())) {
			if (!Objects.equals(environmentName, runningEnvironment)) {
				return null;
			}
			return envValue(key);
		}
		if (!enabled) {
			return defaultValue(key).orElse(null);
		}
		List<ParameterValueEntity> versions = cache.approved(key.name(), environmentName);
		ParameterValueEntity row = inForce(versions, null, businessDate);
		if (row != null) {
			return new ParameterValue<>(key.name(), ParameterValues.convert(key, row.paramValue), row.versionNo,
					row.validFrom, row.environment);
		}
		return defaultValue(key).orElse(null);
	}

	private <T> ParameterValue<T> resolve(ParameterKey<T> key, String productGroup, LocalDate businessDate) {
		if (key.secret()) {
			throw new SecretNotServedException(key.name());
		}
		if ("PRODUCT".equals(key.scope())) {
			throw new ParameterNotInForceException(key.name());
		}
		if ("ENV".equals(key.valueSource())) {
			return envValue(key);
		}
		if (enabled) {
			List<ParameterValueEntity> versions = cache.approved(key.name(), runningEnvironment);
			if (productGroup != null) {
				ParameterValueEntity productRow = inForce(versions, productGroup, businessDate);
				if (productRow != null) {
					return valueOf(key, productRow);
				}
			}
			ParameterValueEntity row = inForce(versions, null, businessDate);
			if (row != null) {
				return valueOf(key, row);
			}
		}
		return defaultValue(key).orElseThrow(() -> new ParameterNotInForceException(key.name()));
	}

	private static ParameterValueEntity inForce(List<ParameterValueEntity> versions, String productGroup,
			LocalDate date) {
		ParameterValueEntity best = null;
		for (ParameterValueEntity candidate : versions) {
			if (!Objects.equals(candidate.productGroup, productGroup)) {
				continue;
			}
			if (candidate.validFrom != null && candidate.validFrom.isAfter(date)) {
				continue;
			}
			if (candidate.validTo != null && candidate.validTo.isBefore(date)) {
				continue;
			}
			if (best == null || candidate.validFrom.isAfter(best.validFrom)) {
				best = candidate;
			}
		}
		return best;
	}

	private <T> ParameterValue<T> valueOf(ParameterKey<T> key, ParameterValueEntity row) {
		return new ParameterValue<>(key.name(), ParameterValues.convert(key, row.paramValue), row.versionNo,
				row.validFrom, row.environment);
	}

	private <T> ParameterValue<T> envValue(ParameterKey<T> key) {
		String text = environment.getProperty(key.envProperty());
		if (text != null && !text.isBlank()) {
			return new ParameterValue<>(key.name(), ParameterValues.convert(key, text.trim()), 0, null,
					runningEnvironment);
		}
		return defaultValue(key).orElseThrow(() -> new ParameterNotInForceException(key.name()));
	}

	private <T> Optional<ParameterValue<T>> defaultValue(ParameterKey<T> key) {
		if (key.defaultValue() == null || key.defaultValue().isEmpty()) {
			return Optional.empty();
		}
		return Optional.of(new ParameterValue<>(key.name(), ParameterValues.convert(key, key.defaultValue()), 0, null,
				runningEnvironment));
	}

	static String typeName(Class<?> type) {
		if (type == Integer.class) {
			return "INTEGER";
		}
		if (type == java.math.BigDecimal.class) {
			return "DECIMAL";
		}
		if (type == Boolean.class) {
			return "BOOLEAN";
		}
		if (type == java.time.LocalDate.class) {
			return "DATE";
		}
		if (type == java.time.LocalTime.class) {
			return "TIME";
		}
		if (type == java.time.Duration.class) {
			return "DURATION";
		}
		if (type == List.class) {
			return "CODE_LIST";
		}
		return "STRING";
	}
}
