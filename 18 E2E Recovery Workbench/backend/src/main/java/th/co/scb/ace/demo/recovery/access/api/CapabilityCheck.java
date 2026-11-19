package th.co.scb.ace.demo.recovery.access.api;

import org.springframework.security.core.Authentication;

/**
 * The capability seam the method check names (SPEC-RWB-E1-042-020). The interim implementation is
 * {@code access.internal.InterimCapabilityCheck}, registered as bean {@code capabilityCheck}.
 */
public interface CapabilityCheck {

	boolean has(Authentication authentication, String area, String right);

	/** True, or throws an {@link ApiProblemException} with {@code ApiError.NOT_PERMITTED}. */
	boolean require(Authentication authentication, String area, String right, String action);
}