package th.co.scb.ace.demo.recovery.casewf.config;

import java.time.LocalDate;
import java.util.NoSuchElementException;

import org.springframework.stereotype.Component;

import th.co.scb.ace.demo.recovery.access.api.CatalogParameterReader;
import th.co.scb.ace.demo.recovery.casewf.config.api.BusinessDateProvider;
import th.co.scb.ace.demo.recovery.casewf.config.api.ParameterKey;
import th.co.scb.ace.demo.recovery.casewf.config.api.ParameterKeys;
import th.co.scb.ace.demo.recovery.casewf.config.api.ParameterNotInForceException;
import th.co.scb.ace.demo.recovery.casewf.config.api.ParameterService;
import th.co.scb.ace.demo.recovery.casewf.config.api.ParameterValue;
import th.co.scb.ace.demo.recovery.casewf.config.api.SecretNotServedException;

/**
 * The P4 read seam of D-RUN-19: code outside P3 reads a catalog parameter here and nowhere else.
 * Always registered whatever the flag. It delegates to {@link ParameterService}, logs nothing and
 * caches nothing of its own, and it throws only JDK exception types so a P1, P2 or P4 caller needs no
 * P3 type. Every message holds the key only (SPEC-RWB-E1-042-026, TC-46).
 */
@Component
class CatalogParameterReaderImpl implements CatalogParameterReader {

	private final ParameterService service;

	private final BusinessDateProvider businessDate;

	CatalogParameterReaderImpl(ParameterService service, BusinessDateProvider businessDate) {
		this.service = service;
		this.businessDate = businessDate;
	}

	@Override
	public <T> Value<T> get(String key, Class<T> type, LocalDate businessDate) {
		ParameterKey<T> definition = definition(key, type);
		try {
			ParameterValue<T> value = service.get(definition, businessDate);
			return new Value<>(value.key(), value.value(), value.versionNo(), value.validFrom(),
					value.environment());
		}
		catch (SecretNotServedException ex) {
			throw new IllegalStateException(key);
		}
		catch (ParameterNotInForceException ex) {
			throw new NoSuchElementException(key);
		}
	}

	@Override
	public <T> Value<T> get(String key, Class<T> type) {
		return get(key, type, businessDate.today());
	}

	private static <T> ParameterKey<T> definition(String key, Class<T> type) {
		ParameterKey<T> definition = ParameterKeys.byName(key, type)
			.orElseThrow(() -> new IllegalArgumentException(key));
		if ("PRODUCT".equals(definition.scope())) {
			throw new IllegalArgumentException(key);
		}
		return definition;
	}
}