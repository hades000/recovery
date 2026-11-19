package th.co.scb.ace.demo.recovery.casewf.migration;

import jakarta.validation.constraints.NotNull;
import jakarta.validation.constraints.Pattern;

import org.springframework.boot.context.properties.ConfigurationProperties;
import org.springframework.validation.annotation.Validated;

/**
 * RWB-TE-001 SPEC-023: {@code rwb.schema} and {@code rwb.flyway.*}, read by the recovery Flyway
 * bean only. Keys and defaults are those of the former shared record.
 *
 * <p>SPEC-RWB-E1-044-002 (D-RCV-28): the schema is pinned to {@code recovery} when Spring binds the
 * record. The constraint is on {@code schema} only, so no nested value is read, and there is no
 * compact-constructor check: building the record in code is unaffected (T-044-08 case (6)).
 */
@ConfigurationProperties(prefix = "rwb")
@Validated
record RecoveryMigrationProperties(
		@NotNull(message = "rwb.schema must be recovery (D-RCV-28)") @Pattern(regexp = "recovery",
				message = "rwb.schema must be recovery (D-RCV-28)") String schema,
		Flyway flyway) {

	/** The recovery Flyway bean runs as the migration account, not the service identity. */
	record Flyway(boolean enabled, String url, String user, String password, String location) {
	}

}
