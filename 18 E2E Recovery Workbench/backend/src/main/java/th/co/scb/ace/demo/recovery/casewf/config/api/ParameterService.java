package th.co.scb.ace.demo.recovery.casewf.config.api;

import java.time.LocalDate;

/** Read a catalog parameter for a business date (SPEC-RWB-E1-042-007, -017). */
public interface ParameterService {

	/** The value in force for the running environment on {@code businessDate}. */
	<T> ParameterValue<T> get(ParameterKey<T> key, LocalDate businessDate);

	/** The product-group row first, then the GLOBAL row (SPEC-RWB-E1-042-007). */
	<T> ParameterValue<T> get(ParameterKey<T> key, String productGroup, LocalDate businessDate);

	/** The catalog-only view of a key, with no value (SPEC-RWB-E1-042-017). */
	CatalogEntry entry(String key);
}