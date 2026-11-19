package th.co.scb.ace.demo.recovery.architecture.boundary;

import java.util.List;
import java.util.Optional;

/**
 * RWB-TE-001 SPEC-002, SPEC-003 (BR6): immutable model of the module map. The map is the only
 * source of module names, packages, published packages, client packages and client libraries.
 */
public record ModuleMap(String source, String rootPackage, List<Module> modules, List<External> external,
		List<String> clientLibraries, Object sourceViews) {

	public ModuleMap {
		modules = List.copyOf(modules);
		external = List.copyOf(external);
		clientLibraries = List.copyOf(clientLibraries);
	}

	/** One nested design module of the recovery module (P1..P10, S1..S9). */
	public record Module(String code, String name, List<String> published, List<String> clientPackages) {

		public Module {
			published = List.copyOf(published);
			clientPackages = List.copyOf(clientPackages);
		}
	}

	/** One module outside the recovery root whose published packages may be used. */
	public record External(String name, String rootPackage, List<String> published) {

		public External {
			published = List.copyOf(published);
		}
	}

	public String modulePackage(Module module) {
		return rootPackage + "." + module.name();
	}

	/** The module whose package equals {@code packageName} or is a prefix of it. */
	public Optional<Module> moduleOf(String packageName) {
		return modules.stream()
			.filter(module -> packageName.equals(modulePackage(module))
					|| packageName.startsWith(modulePackage(module) + "."))
			.findFirst();
	}
}
