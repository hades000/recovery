package th.co.scb.ace.demo.recovery.casewf.config.api;

import java.time.LocalDate;

/**
 * A value in force, or a catalog default with {@code versionNo 0} and {@code validFrom null}
 * (SPEC-RWB-E1-042-007).
 */
public record ParameterValue<T>(String key, T value, int versionNo, LocalDate validFrom, String environment) {
}