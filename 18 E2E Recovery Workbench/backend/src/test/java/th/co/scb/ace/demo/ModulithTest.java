package th.co.scb.ace.demo;

import org.junit.jupiter.api.Test;
import org.springframework.modulith.core.ApplicationModules;
import org.springframework.modulith.docs.Documenter;

/**
 * BND-3/BND-4: a module reaches another only through its {@code api} named interface, and no
 * module uses another's internal types. Also writes the module diagrams to build/spring-modulith-docs.
 */
class ModulithTest {

	private final ApplicationModules modules = ApplicationModules.of(AceRecoveryApplication.class);

	@Test
	void modulesRespectTheirBoundaries() {
		modules.verify();
	}

	@Test
	void writeModuleDocumentation() {
		new Documenter(modules).writeModulesAsPlantUml().writeIndividualModulesAsPlantUml();
	}
}
