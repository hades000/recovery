package th.co.scb.ace.demo.recovery.casewf.migration;

import java.util.Map;

import javax.sql.DataSource;

import org.flywaydb.core.Flyway;
import org.springframework.boot.autoconfigure.condition.ConditionalOnProperty;
import org.springframework.boot.jdbc.autoconfigure.DataSourceProperties;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import org.springframework.util.StringUtils;

/**
 * The recovery module's own Flyway bean (BS-2.3, D-RCV-18/28). In ACE it is initialised after the
 * ACE core bean; here there is no core bean, so Spring Boot's Flyway auto-configuration is off.
 *
 * <p>Runs as the migration account ({@code rwb.flyway.user}) when one is set, so the service
 * identity never holds DDL rights. {@code clean} is disabled in every environment (NFR-027).
 *
 * <p>SPEC-RWB-E1-044-002: the properties record is registered by {@link MigrationPropertiesConfig},
 * which has no condition, so the schema pin also holds when this configuration is switched off.
 */
@Configuration(proxyBeanMethods = false)
@ConditionalOnProperty(name = "rwb.flyway.enabled", havingValue = "true", matchIfMissing = true)
class RecoveryFlywayConfig {

	static final String HISTORY_TABLE = "flyway_schema_history_recovery";

	@Bean
	Flyway recoveryFlyway(RecoveryMigrationProperties properties, DataSource dataSource, DataSourceProperties dataSourceProperties) {
		RecoveryMigrationProperties.Flyway flyway = properties.flyway();
		String schema = properties.schema();

		var configuration = Flyway.configure()
				.schemas(schema)
				.defaultSchema(schema)
				.table(HISTORY_TABLE)
				.locations(flyway.location())
				.placeholders(Map.of("recoverySchema", schema))
				.outOfOrder(false)
				.baselineVersion("0")
				.baselineOnMigrate(true)
				.cleanDisabled(true)
				.createSchemas(false)
				.validateMigrationNaming(true)
				.validateOnMigrate(true)
				.callbacks(new RecoveryMigrationRunner.FailedVersion());

		if (StringUtils.hasText(flyway.user())) {
			String url = StringUtils.hasText(flyway.url()) ? flyway.url() : dataSourceProperties.determineUrl();
			configuration.dataSource(url, flyway.user(), flyway.password());
		}
		else {
			configuration.dataSource(dataSource);
		}
		return configuration.load();
	}

	/**
	 * SPEC-RWB-E1-044-003: the factory never migrates; this bean does it when the container
	 * initialises it, so a test that calls {@code recoveryFlyway(...)} directly runs no migration.
	 */
	@Bean(initMethod = "migrate")
	RecoveryMigrationRunner recoveryMigrationRunner(Flyway recoveryFlyway, RecoveryMigrationProperties properties) {
		return new RecoveryMigrationRunner(recoveryFlyway, properties);
	}
}
