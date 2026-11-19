package th.co.scb.ace.demo.recovery.casewf.rules;

import static org.assertj.core.api.Assertions.assertThat;

import org.junit.jupiter.api.Test;

import th.co.scb.ace.demo.recovery.testsupport.ApplicationYamlEnvironment;

/**
 * RWB-TE-001 T-TE001-12 (SPEC-023): {@code rwb.drools.kiebase-cache-max} binds from
 * {@code application.yaml} without the process environment.
 */
class DroolsPropertiesTest {

	@Test
	void bindsCacheMaxFromApplicationYaml() {
		ApplicationYamlEnvironment.runner().withUserConfiguration(DroolsProperties.Registration.class).run(context -> {
			assertThat(context).hasNotFailed();
			assertThat(context.getBean(DroolsProperties.class).kiebaseCacheMax()).isEqualTo(20);
		});
	}
}
