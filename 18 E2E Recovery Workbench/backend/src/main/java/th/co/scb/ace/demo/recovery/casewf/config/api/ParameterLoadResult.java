package th.co.scb.ace.demo.recovery.casewf.config.api;

import java.time.LocalDate;
import java.util.UUID;

/** One PARAMETER load, as RWB-E1-043 renders it into API v4 {@code ReferenceLoad} (SPEC-RWB-E1-042-017). */
public record ParameterLoadResult(UUID loadId, String table, LocalDate validFrom, String status, int rows,
		boolean repeat) {
}