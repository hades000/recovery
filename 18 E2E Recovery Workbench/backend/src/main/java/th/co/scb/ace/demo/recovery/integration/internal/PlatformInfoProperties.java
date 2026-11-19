package th.co.scb.ace.demo.recovery.integration.internal;

import jakarta.validation.constraints.NotNull;
import jakarta.validation.constraints.Pattern;

import org.springframework.boot.context.properties.ConfigurationProperties;
import org.springframework.validation.annotation.Validated;

/**
 * RWB-TE-001 SPEC-023: {@code rwb.environment} and {@code rwb.schema}, the environment the platform
 * info endpoint reports. Keys and defaults are those of the former shared record.
 *
 * <p>REVIEW-001 H2: {@code rwb.environment} has no default and must be one of DEV, SIT, UAT or PROD,
 * so a service with {@code RWB_ENVIRONMENT} unset or misspelt stops at startup instead of serving the
 * DEV parameter values. This record is registered unconditionally, so the check runs in every
 * deployment.
 */
@ConfigurationProperties(prefix = "rwb")
@Validated
record PlatformInfoProperties(
		@NotNull(message = "rwb.environment (RWB_ENVIRONMENT) must be DEV, SIT, UAT or PROD") @Pattern(
				regexp = "DEV|SIT|UAT|PROD",
				message = "rwb.environment (RWB_ENVIRONMENT) must be DEV, SIT, UAT or PROD") String environment,
		String schema) {
}
