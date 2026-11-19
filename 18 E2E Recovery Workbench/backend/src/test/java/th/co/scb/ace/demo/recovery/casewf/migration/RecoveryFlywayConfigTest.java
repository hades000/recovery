package th.co.scb.ace.demo.recovery.casewf.migration;

import static org.assertj.core.api.Assertions.assertThat;
import static org.mockito.Mockito.mock;

import javax.sql.DataSource;

import org.flywaydb.core.Flyway;
import org.junit.jupiter.api.Test;
import org.springframework.boot.jdbc.autoconfigure.DataSourceProperties;

import th.co.scb.ace.demo.recovery.testsupport.ApplicationYamlEnvironment;

/**
 * RWB-TE-001 SPEC-024: the recovery Flyway bean keeps its schema, history table, placeholder and
 * clean-disabled rule, and runs as the migration account only when one is configured.
 */
class RecoveryFlywayConfigTest {

	private static final String LOCATION = "classpath:db/modulemigration/recovery";

	private static final String SERVICE_URL = "jdbc:postgresql://localhost:5433/ace";

	@Test
	void bindsSchemaAndFlywayFromApplicationYaml() {
		ApplicationYamlEnvironment.runner()
			.withUserConfiguration(PropertiesRegistration.class, MigrationPropertiesConfig.class)
			.run(context -> {
			assertThat(context).hasNotFailed();
			RecoveryMigrationProperties properties = context.getBean(RecoveryMigrationProperties.class);
			assertThat(properties.schema()).isEqualTo("recovery");
			assertThat(properties.flyway().enabled()).isTrue();
			assertThat(properties.flyway().url()).isEqualTo(SERVICE_URL);
			assertThat(properties.flyway().user()).isEqualTo("rwb_migrator");
			assertThat(properties.flyway().password()).isEmpty();
			assertThat(properties.flyway().location()).isEqualTo(LOCATION);
		});
	}

	@Test
	void recoveryFlywayKeepsSchemaHistoryPlaceholderAndCleanDisabled() {
		Flyway flyway = config().recoveryFlyway(properties(new RecoveryMigrationProperties.Flyway(true,
				"jdbc:postgresql://localhost:5433/ace", "rwb_migrator", "synthetic-password", LOCATION)),
				mock(DataSource.class), dataSourceProperties());

		assertThat(flyway.getConfiguration().getSchemas()).containsExactly("recovery");
		assertThat(flyway.getConfiguration().getDefaultSchema()).isEqualTo("recovery");
		assertThat(flyway.getConfiguration().getTable()).isEqualTo("flyway_schema_history_recovery");
		assertThat(flyway.getConfiguration().getPlaceholders()).containsEntry("recoverySchema", "recovery");
		assertThat(flyway.getConfiguration().isCleanDisabled()).isTrue();
		assertThat(flyway.getConfiguration().getLocations()[0].getDescriptor()).isEqualTo(LOCATION);
		assertThat(flyway.getConfiguration().getCallbacks())
			.hasExactlyElementsOfTypes(RecoveryMigrationRunner.FailedVersion.class);
	}

	@Test
	void migrationAccountWithItsOwnUrlBecomesTheFlywayDataSource() {
		Flyway flyway = config().recoveryFlyway(properties(new RecoveryMigrationProperties.Flyway(true,
				"jdbc:postgresql://migrator:5433/ace", "rwb_migrator", "", LOCATION)), mock(DataSource.class),
				dataSourceProperties());

		assertThat(flyway.getConfiguration().getUrl()).isEqualTo("jdbc:postgresql://migrator:5433/ace");
		assertThat(flyway.getConfiguration().getUser()).isEqualTo("rwb_migrator");
	}

	@Test
	void migrationAccountWithoutItsOwnUrlFallsBackToTheServiceUrl() {
		Flyway flyway = config().recoveryFlyway(properties(
				new RecoveryMigrationProperties.Flyway(true, "", "rwb_migrator", "", LOCATION)), mock(DataSource.class),
				dataSourceProperties());

		assertThat(flyway.getConfiguration().getUrl()).isEqualTo(SERVICE_URL);
		assertThat(flyway.getConfiguration().getUser()).isEqualTo("rwb_migrator");
	}

	@Test
	void noMigrationAccountUsesTheServiceDataSource() {
		DataSource dataSource = mock(DataSource.class);

		Flyway flyway = config().recoveryFlyway(
				properties(new RecoveryMigrationProperties.Flyway(true, SERVICE_URL, "", "", LOCATION)), dataSource,
				dataSourceProperties());

		assertThat(flyway.getConfiguration().getDataSource()).isSameAs(dataSource);
	}

	private static RecoveryFlywayConfig config() {
		return new RecoveryFlywayConfig();
	}

	private static RecoveryMigrationProperties properties(RecoveryMigrationProperties.Flyway flyway) {
		return new RecoveryMigrationProperties("recovery", flyway);
	}

	private static DataSourceProperties dataSourceProperties() {
		DataSourceProperties properties = new DataSourceProperties();
		properties.setUrl(SERVICE_URL);
		return properties;
	}

	@org.springframework.context.annotation.Configuration(proxyBeanMethods = false)
	@org.springframework.boot.context.properties.EnableConfigurationProperties(RecoveryMigrationProperties.class)
	static class PropertiesRegistration {
	}
}
