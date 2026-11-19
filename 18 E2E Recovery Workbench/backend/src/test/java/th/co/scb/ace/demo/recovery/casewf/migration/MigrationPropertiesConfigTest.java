package th.co.scb.ace.demo.recovery.casewf.migration;

import static org.assertj.core.api.Assertions.assertThat;
import static org.assertj.core.api.Assertions.assertThatCode;

import java.util.ArrayList;
import java.util.List;
import java.util.Map;

import org.flywaydb.core.Flyway;
import org.flywaydb.core.api.FlywayException;
import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.NoSuchBeanDefinitionException;
import org.springframework.boot.context.properties.ConfigurationPropertiesBindException;
import org.springframework.boot.context.properties.bind.validation.BindValidationException;
import org.springframework.boot.test.context.runner.ApplicationContextRunner;
import org.springframework.core.env.SystemEnvironmentPropertySource;

/**
 * SPEC-RWB-E1-044-002 (T-044-08, audit A-17, CLAR-009): {@code rwb.schema} is pinned to
 * {@code recovery} when the migration properties record binds, whatever {@code rwb.flyway.enabled}
 * is, and building the record in code is unaffected (no compact-constructor check).
 */
class MigrationPropertiesConfigTest {

	private static final String SCHEMA = "rwb.schema";

	private static final String RECOVERY = "recovery";

	private static final String WRONG = "rwb_case";

	private final ApplicationContextRunner runner = new ApplicationContextRunner()
		.withUserConfiguration(MigrationPropertiesConfig.class, RecoveryFlywayConfig.class);

	@Test
	void flywayOffWithAWrongSchemaFailsAtPropertiesBinding() {
		assertBindingFails(runner.withPropertyValues("rwb.flyway.enabled=false", SCHEMA + "=" + WRONG), WRONG);
	}

	@Test
	void flywayOnWithAWrongSchemaFailsAtPropertiesBinding() {
		assertBindingFails(runner.withPropertyValues("rwb.flyway.enabled=true", SCHEMA + "=" + WRONG), WRONG);
	}

	@Test
	void relaxedBindingFromTheEnvironmentCannotOverrideTheSchema() {
		ApplicationContextRunner environmentRunner = new ApplicationContextRunner()
			.withInitializer(context -> context.getEnvironment()
				.getPropertySources()
				.addFirst(new SystemEnvironmentPropertySource("systemEnvironment",
						Map.of("RWB_FLYWAY_ENABLED", "false", "RWB_SCHEMA", WRONG))))
			.withUserConfiguration(MigrationPropertiesConfig.class, RecoveryFlywayConfig.class);

		assertBindingFails(environmentRunner, WRONG);
	}

	@Test
	void aBlankSchemaFailsWithThePinnedPattern() {
		assertBindingFails(runner.withPropertyValues("rwb.flyway.enabled=false", SCHEMA + "="), null);
	}

	/** CONF-E044-05: {@code @NotNull} is what refuses an absent schema. */
	@Test
	void anAbsentSchemaFailsAtPropertiesBinding() {
		assertBindingFails(runner.withPropertyValues("rwb.flyway.enabled=false"), null);
	}

	/** CONF-E044-05: the pattern is case-sensitive; the schema is exactly {@code recovery} (D-RCV-28). */
	@Test
	void aSchemaThatDiffersOnlyInCaseFailsAtPropertiesBinding() {
		assertBindingFails(runner.withPropertyValues("rwb.flyway.enabled=false", SCHEMA + "=Recovery"), "Recovery");
	}

	@Test
	void flywayOffWithThePinnedSchemaStartsAndCreatesNoFlywayBean() {
		runner.withPropertyValues("rwb.flyway.enabled=false", SCHEMA + "=" + RECOVERY).run(context -> {
			assertThat(context).hasNotFailed();
			assertThat(context.getBeansOfType(RecoveryMigrationProperties.class)).hasSize(1);
			assertThat(context.getBean(RecoveryMigrationProperties.class).schema()).isEqualTo(RECOVERY);
			assertThat(context.getBeansOfType(Flyway.class)).isEmpty();
		});
	}

	@Test
	void directConstructionOfTheRecordIsNotValidated() {
		assertThatCode(() -> new RecoveryMigrationProperties(WRONG, null)).doesNotThrowAnyException();
		assertThatCode(() -> new RecoveryMigrationProperties("", null)).doesNotThrowAnyException();
		assertThatCode(() -> new RecoveryMigrationProperties(null, null)).doesNotThrowAnyException();
	}

	private static void assertBindingFails(ApplicationContextRunner runner, String rejectedValue) {
		runner.run(context -> {
			assertThat(context).hasFailed();
			List<Throwable> chain = causes(context.getStartupFailure());
			assertThat(chain).anyMatch(ConfigurationPropertiesBindException.class::isInstance);
			assertThat(chain).filteredOn(ConfigurationPropertiesBindException.class::isInstance)
				.singleElement()
				.satisfies(failure -> assertThat(((ConfigurationPropertiesBindException) failure).getBeanType())
					.isEqualTo(RecoveryMigrationProperties.class));
			Throwable root = chain.get(chain.size() - 1);
			assertThat(root).isInstanceOf(BindValidationException.class);
			assertThat(root.getMessage()).contains(SCHEMA).contains("D-RCV-28");
			if (rejectedValue != null) {
				assertThat(root.getMessage()).contains("[" + rejectedValue + "]");
			}
			assertThat(chain).noneMatch(NullPointerException.class::isInstance)
				.noneMatch(FlywayException.class::isInstance)
				.noneMatch(NoSuchBeanDefinitionException.class::isInstance);
		});
	}

	private static List<Throwable> causes(Throwable failure) {
		List<Throwable> chain = new ArrayList<>();
		Throwable current = failure;
		while (current != null && !chain.contains(current)) {
			chain.add(current);
			current = current.getCause();
		}
		return chain;
	}

}
