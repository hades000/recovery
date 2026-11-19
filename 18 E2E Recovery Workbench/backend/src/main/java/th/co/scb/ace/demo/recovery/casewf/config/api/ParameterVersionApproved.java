package th.co.scb.ace.demo.recovery.casewf.config.api;

import java.time.Instant;
import java.time.LocalDate;
import java.util.List;
import java.util.UUID;

/**
 * Published in process after an approval commits (SPEC-RWB-E1-042-018). No approver ID and no
 * personal data travel in it.
 */
public record ParameterVersionApproved(UUID loadId, List<String> paramKeys, LocalDate validFrom,
		List<Version> versions, Instant occurredAt) {

	public ParameterVersionApproved {
		paramKeys = List.copyOf(paramKeys);
		versions = List.copyOf(versions);
	}

	/** One approved version: a key, its environment and the version number. */
	public record Version(String paramKey, String environment, int versionNo) {
	}
}