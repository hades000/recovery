package th.co.scb.ace.demo.recovery.integration.flags.api;

/**
 * Feature flags that switch whole platform paths (ADR-008). A flag that is off returns the
 * previous code path (BS-6.7).
 *
 * @param temporal {@code rwb.p3.temporal}: starts the Temporal worker and the Temporal admin API
 * @param drools   {@code rwb.p3.drools}: enables the Drools rule engine and the rule package API
 */
public record RecoveryFlags(boolean temporal, boolean drools) {
}
