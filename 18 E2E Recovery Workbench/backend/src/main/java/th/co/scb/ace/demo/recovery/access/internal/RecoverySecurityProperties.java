package th.co.scb.ace.demo.recovery.access.internal;

import java.util.List;

import org.springframework.boot.context.properties.ConfigurationProperties;

/**
 * RWB-TE-001 SPEC-023: {@code rwb.security.*}, read by the resource-server configuration only. Keys
 * and defaults are those of the former shared record.
 */
@ConfigurationProperties(prefix = "rwb.security")
record RecoverySecurityProperties(String issuer, String jwkSetUri, String audience, String rolesClaim,
		List<String> corsOrigins) {
}
