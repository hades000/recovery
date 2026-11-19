package th.co.scb.ace.demo.recovery.integration.internal;

import static org.assertj.core.api.Assertions.assertThat;
import static org.mockito.ArgumentMatchers.anyString;
import static org.mockito.ArgumentMatchers.eq;
import static org.mockito.Mockito.mock;
import static org.mockito.Mockito.when;

import org.junit.jupiter.api.Test;
import org.springframework.jdbc.core.JdbcTemplate;

import th.co.scb.ace.demo.recovery.integration.flags.api.RecoveryFlags;
import th.co.scb.ace.demo.recovery.testsupport.ApplicationYamlEnvironment;

/**
 * RWB-TE-001 SPEC-024: {@code PlatformInfoController} reports the environment, the flags and the
 * counts the service identity can see, and its properties bind from {@code application.yaml}.
 */
class PlatformInfoControllerTest {

	/** REVIEW-001 H2: the environment comes from RWB_ENVIRONMENT; there is no DEV default any more. */
	@Test
	void bindsEnvironmentAndSchemaFromApplicationYaml() {
		ApplicationYamlEnvironment.runner()
			.withUserConfiguration(PlatformInfoController.Registration.class)
			.withPropertyValues("RWB_ENVIRONMENT=SIT")
			.run(context -> {
				assertThat(context).hasNotFailed();
				PlatformInfoProperties properties = context.getBean(PlatformInfoProperties.class);
				assertThat(properties.environment()).isEqualTo("SIT");
				assertThat(properties.schema()).isEqualTo("recovery");
			});
	}

	/** REVIEW-001 H2: an unset RWB_ENVIRONMENT stops the service at startup instead of serving DEV values. */
	@Test
	void aMissingEnvironmentFailsAtStartup() {
		ApplicationYamlEnvironment.runner().withUserConfiguration(PlatformInfoController.Registration.class).run(context -> {
			assertThat(context).hasFailed();
			assertThat(context.getStartupFailure()).rootCause().hasMessageContaining("rwb.environment");
		});
	}

	/** REVIEW-001 H2: a value outside DEV/SIT/UAT/PROD, such as a wrong-case "prod", stops the service. */
	@Test
	void anEnvironmentOutsideTheListFailsAtStartup() {
		ApplicationYamlEnvironment.runner()
			.withUserConfiguration(PlatformInfoController.Registration.class)
			.withPropertyValues("RWB_ENVIRONMENT=prod")
			.run(context -> {
				assertThat(context).hasFailed();
				assertThat(context.getStartupFailure()).rootCause().hasMessageContaining("rwb.environment");
			});
	}

	@Test
	void infoReportsTheEnvironmentFlagsAndDatabaseCounts() {
		JdbcTemplate jdbc = mock(JdbcTemplate.class);
		when(jdbc.queryForObject(anyString(), eq(Integer.class), eq("recovery"))).thenReturn(2, 5);
		when(jdbc.queryForObject(anyString(), eq(Integer.class))).thenReturn(0);
		PlatformInfoController controller = new PlatformInfoController(
				new PlatformInfoProperties("DEV", "recovery"), new RecoveryFlags(true, false), jdbc);

		PlatformInfoController.PlatformInfo info = controller.info();

		assertThat(info.service()).isEqualTo("ace-recovery");
		assertThat(info.environment()).isEqualTo("DEV");
		assertThat(info.flags().temporal()).isTrue();
		assertThat(info.flags().drools()).isFalse();
		assertThat(info.database().schema()).isEqualTo("recovery");
		assertThat(info.database().aceViews()).isEqualTo(2);
		assertThat(info.database().recoveryTables()).isEqualTo(5);
		assertThat(info.database().visiblePublicTables()).isZero();
	}
}
