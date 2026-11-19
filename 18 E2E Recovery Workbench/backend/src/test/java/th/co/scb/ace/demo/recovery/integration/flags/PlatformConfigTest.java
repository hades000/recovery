package th.co.scb.ace.demo.recovery.integration.flags;

import static org.assertj.core.api.Assertions.assertThat;

import org.junit.jupiter.api.Test;

import th.co.scb.ace.demo.recovery.integration.flags.api.RecoveryFlags;
import th.co.scb.ace.demo.recovery.testsupport.ApplicationYamlEnvironment;

/**
 * RWB-TE-001 SPEC-024: the {@code RecoveryFlags} bean carries the {@code rwb.p3} values from the
 * bound properties, both on and off.
 */
class PlatformConfigTest {

	@Test
	void bindsFlagsFromApplicationYaml() {
		ApplicationYamlEnvironment.runner().withUserConfiguration(PlatformConfig.class).run(context -> {
			assertThat(context).hasNotFailed();
			RecoveryFlags flags = context.getBean(RecoveryFlags.class);
			assertThat(flags.temporal()).isFalse();
			assertThat(flags.drools()).isFalse();
		});
	}

	@Test
	void flagsCarryThePropertiesWhenBothAreOn() {
		ApplicationYamlEnvironment.runner()
			.withUserConfiguration(PlatformConfig.class)
			.withPropertyValues("rwb.p3.temporal=true", "rwb.p3.drools=true")
			.run(context -> {
				assertThat(context).hasNotFailed();
				RecoveryFlags flags = context.getBean(RecoveryFlags.class);
				assertThat(flags.temporal()).isTrue();
				assertThat(flags.drools()).isTrue();
			});
	}
}
