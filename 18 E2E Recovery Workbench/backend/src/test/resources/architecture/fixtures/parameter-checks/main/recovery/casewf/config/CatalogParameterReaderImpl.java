package recovery.casewf.config;

import java.time.LocalDate;
import th.co.scb.ace.demo.recovery.access.api.CatalogParameterReader;

/** Fixture for TC-E1-042-03 (i): the implementation is skipped by path. Not compiled. */
class CatalogParameterReaderImpl implements CatalogParameterReader {

	private final String key;

	CatalogParameterReaderImpl(String key) {
		this.key = key;
	}

	@Override
	public <T> Value<T> get(String key, Class<T> type, LocalDate businessDate) {
		return get(key, type, businessDate);
	}

	@Override
	public <T> Value<T> get(String key, Class<T> type) {
		return get(key, type, LocalDate.now());
	}
}