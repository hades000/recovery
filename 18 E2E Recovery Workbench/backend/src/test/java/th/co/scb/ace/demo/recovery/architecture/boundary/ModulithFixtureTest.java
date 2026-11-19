package th.co.scb.ace.demo.recovery.architecture.boundary;

import static org.assertj.core.api.Assertions.assertThat;
import static org.assertj.core.api.Assertions.assertThatThrownBy;

import java.util.List;

import org.junit.jupiter.api.Test;
import org.springframework.modulith.core.ApplicationModule;
import org.springframework.modulith.core.ApplicationModules;

/**
 * RWB-TE-001 T-TE001-16, TC-TE-001-03 (SPEC-007, AC3, BR3): Spring Modulith's own verify() fails an
 * internal cross-module dependency and a cycle, and passes a dependency on a published interface.
 */
class ModulithFixtureTest {

	private static final String FIXTURES = "th.co.scb.ace.boundaryfixture";

	private static ApplicationModules modules(String world) {
		return ApplicationModules.of(FIXTURES + "." + world, location -> true);
	}

	private static List<String> modulePackages(ApplicationModules modules) {
		return modules.stream().map(ApplicationModule::getBasePackage).map(pkg -> pkg.getName()).toList();
	}

	@Test
	void internalDependencyBetweenModulesFailsVerify() {
		ApplicationModules modules = modules("bnd3fail");

		assertThat(modulePackages(modules)).contains(FIXTURES + ".bnd3fail.recovery",
				FIXTURES + ".bnd3fail.recovery.integration", FIXTURES + ".bnd3fail.recovery.decision");
		assertThatThrownBy(modules::verify).hasMessageContaining("DecisionLogRepository");
	}

	@Test
	void publishedWriterDependencyPassesVerify() {
		ApplicationModules modules = modules("bnd3pass");

		assertThat(modulePackages(modules)).contains(FIXTURES + ".bnd3pass.recovery",
				FIXTURES + ".bnd3pass.recovery.integration", FIXTURES + ".bnd3pass.recovery.decision");
		modules.verify();
	}

	@Test
	void cycleBetweenModulesFailsVerify() {
		assertThatThrownBy(modules("bnd3cycle")::verify).hasMessageContaining("cycle");
	}
}
