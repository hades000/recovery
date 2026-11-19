package th.co.scb.ace.demo.recovery.integration.flags;

import org.springframework.boot.context.properties.ConfigurationProperties;

/**
 * RWB-TE-001 SPEC-023: {@code rwb.p3.*}, the feature flags the integration module publishes through
 * {@code RecoveryFlags}. Keys and defaults are those of the former shared record; no module reads
 * another module's settings.
 */
@ConfigurationProperties(prefix = "rwb.p3")
record RecoveryFlagProperties(boolean temporal, boolean drools) {
}
