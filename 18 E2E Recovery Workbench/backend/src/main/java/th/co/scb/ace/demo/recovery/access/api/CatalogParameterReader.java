package th.co.scb.ace.demo.recovery.access.api;

import java.time.LocalDate;

/**
 * The only way code outside P3 reads catalog parameters (D-RUN-19, GR3). Implemented by
 * {@code casewf.config.CatalogParameterReaderImpl}, always registered whatever the flag.
 *
 * <p>It throws only JDK exception types: {@link IllegalArgumentException} for an unknown key, a
 * wrong type or a PRODUCT key; {@link IllegalStateException} for a secret; and
 * {@link java.util.NoSuchElementException} when nothing is in force and there is no default. The
 * message holds the key only.
 */
public interface CatalogParameterReader {

	/** The value in force on {@code businessDate} for the running environment, GLOBAL scope. */
	<T> Value<T> get(String key, Class<T> type, LocalDate businessDate);

	/** The same, on the business date of the business-date provider (SPEC-RWB-E1-042-023). */
	<T> Value<T> get(String key, Class<T> type);

	/** A value in force, or a catalog default with {@code versionNo 0}. */
	record Value<T>(String key, T value, int versionNo, LocalDate validFrom, String environment) {
	}
}