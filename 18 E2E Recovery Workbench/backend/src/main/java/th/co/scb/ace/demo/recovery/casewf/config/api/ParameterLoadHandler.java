package th.co.scb.ace.demo.recovery.casewf.config.api;

import java.io.InputStream;
import java.time.LocalDate;
import java.util.Optional;
import java.util.UUID;

/**
 * The PARAMETER branch of the reference-load endpoint (RWB-E1-043 calls it, D-RUN-10 and D-RUN-20).
 * Every refusal crosses this interface as {@code access.api.ApiProblemException}.
 */
public interface ParameterLoadHandler {

	String TABLE = "PARAMETER";

	ParameterLoadResult load(InputStream csv, LocalDate validFrom, UUID authorUserId);

	ParameterLoadResult approve(UUID loadId, UUID approverUserId);

	ParameterLoadResult rollback(UUID loadId, String reason, UUID userId);

	Optional<ParameterLoadResult> find(UUID loadId);
}