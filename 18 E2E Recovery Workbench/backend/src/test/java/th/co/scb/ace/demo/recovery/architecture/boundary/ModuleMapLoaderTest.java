package th.co.scb.ace.demo.recovery.architecture.boundary;

import static org.assertj.core.api.Assertions.assertThat;
import static org.assertj.core.api.Assertions.assertThatThrownBy;

import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Path;
import java.util.List;
import java.util.Map;

import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.io.TempDir;

/**
 * RWB-TE-001 T-TE001-01 (SPEC-003, BR6): the module map loader reads a valid map into an immutable
 * model and refuses every malformed map with a message that names the file and the field path.
 */
class ModuleMapLoaderTest {

	private static final String VALID = """
			rootPackage: x.recovery
			modules:
			  - { code: P2, name: integration, published: [api, flags.api], clientPackages: [adapter] }
			  - { code: P3, name: casewf, published: [api], clientPackages: [] }
			external:
			  - { name: common, rootPackage: x.common, published: [api] }
			  - { name: collection, rootPackage: x.collection, published: [api] }
			clientLibraries: [java.net.http, com.azure.storage]
			""";

	@TempDir
	Path dir;

	private Path write(String yaml) throws IOException {
		return Files.writeString(dir.resolve("map.yaml"), yaml);
	}

	private void assertRejected(String yaml, String fieldPath, String problem) throws IOException {
		Path file = write(yaml);
		assertThatThrownBy(() -> ModuleMapLoader.load(file))
				.isInstanceOf(IllegalStateException.class)
				.hasMessageStartingWith("map.yaml: " + fieldPath + ": ")
				.hasMessageContaining(problem);
	}

	@Test
	void loadsAValidMap() throws IOException {
		ModuleMap map = ModuleMapLoader.load(write(VALID));

		assertThat(map.source()).isEqualTo("map.yaml");
		assertThat(map.rootPackage()).isEqualTo("x.recovery");
		assertThat(map.modules()).containsExactly(
				new ModuleMap.Module("P2", "integration", List.of("api", "flags.api"), List.of("adapter")),
				new ModuleMap.Module("P3", "casewf", List.of("api"), List.of()));
		assertThat(map.external()).containsExactly(
				new ModuleMap.External("common", "x.common", List.of("api")),
				new ModuleMap.External("collection", "x.collection", List.of("api")));
		assertThat(map.clientLibraries()).containsExactly("java.net.http", "com.azure.storage");
		assertThat(map.sourceViews()).isNull();
		assertThatThrownBy(() -> map.modules().add(map.modules().getFirst()))
				.isInstanceOf(UnsupportedOperationException.class);
	}

	@Test
	void derivesModulePackagesFromTheMap() throws IOException {
		ModuleMap map = ModuleMapLoader.load(write(VALID));
		ModuleMap.Module casewf = map.modules().get(1);

		assertThat(map.modulePackage(casewf)).isEqualTo("x.recovery.casewf");
		assertThat(map.moduleOf("x.recovery.casewf")).contains(casewf);
		assertThat(map.moduleOf("x.recovery.casewf.internal")).contains(casewf);
		assertThat(map.moduleOf("x.recovery.casewfextra")).isEmpty();
		assertThat(map.moduleOf("x.recovery")).isEmpty();
	}

	@Test
	void loadsTheRealMap() {
		ModuleMap map = ModuleMapLoader.load(Path.of("src/test/resources/architecture/recovery-modules.yaml"));

		assertThat(map.modules()).extracting(ModuleMap.Module::code).containsExactly(
				"P1", "P2", "P3", "P4", "P5", "P6", "P7", "P8", "P9", "P10",
				"S1", "S2", "S3", "S4", "S5", "S6", "S7", "S8", "S9");
		assertThat(map.modules()).extracting(ModuleMap.Module::name).containsExactly(
				"dataengine", "integration", "casewf", "access", "dochub", "comms", "decision", "payments",
				"reporting", "agent", "valuation", "treatment", "guarantee", "litigation", "asset", "debtsale",
				"writeoff", "deviation", "partner");
		for (ModuleMap.Module module : map.modules()) {
			List<String> published = switch (module.name()) {
				case "integration" -> List.of("api", "flags.api");
				case "casewf" -> List.of("api", "config.api", "rules", "timers", "workflow");
				default -> List.of("api");
			};
			List<String> clientPackages = switch (module.name()) {
				case "integration" -> List.of("adapter");
				case "dochub" -> List.of("storage");
				case "agent" -> List.of("client");
				default -> List.of();
			};
			assertThat(module.published()).as(module.name()).isEqualTo(published);
			assertThat(module.clientPackages()).as(module.name()).isEqualTo(clientPackages);
		}
		assertThat(map.external()).extracting(ModuleMap.External::name).containsExactly("common", "collection");
		assertThat(map.clientLibraries()).hasSize(16).doesNotHaveDuplicates();
		assertThat(map.sourceViews()).isNull();
	}

	@Test
	void carriesSourceViewsUnvalidated() throws IOException {
		ModuleMap map = ModuleMapLoader.load(write(VALID + "sourceViews: { anything: [1, two] }\n"));

		assertThat(map.sourceViews()).isEqualTo(Map.of("anything", List.of(1, "two")));
	}

	@Test
	void missingFileNamesTheFile() {
		Path file = dir.resolve("absent.yaml");
		assertThatThrownBy(() -> ModuleMapLoader.load(file))
				.isInstanceOf(IllegalStateException.class)
				.hasMessageStartingWith("absent.yaml: $: ")
				.hasMessageContaining("cannot read");
	}

	@Test
	void invalidYamlNamesTheFile() throws IOException {
		assertRejected("rootPackage: [unclosed\n", "$", "invalid YAML");
	}

	@Test
	void emptyOrScalarDocumentIsRejected() throws IOException {
		assertRejected("", "$", "must be a mapping");
		assertRejected("just text\n", "$", "must be a mapping");
	}

	@Test
	void duplicateYamlKeyIsRejected() throws IOException {
		assertRejected(VALID + "rootPackage: y.recovery\n", "$", "duplicate key");
	}

	@Test
	void missingRequiredFieldNamesThePath() throws IOException {
		assertRejected(VALID.replace("rootPackage: x.recovery\n", ""), "rootPackage", "required");
		assertRejected(VALID.replace("code: P3, ", ""), "modules[1].code", "required");
		assertRejected(VALID.replace(", clientPackages: []", ""), "modules[1].clientPackages", "required");
		assertRejected(VALID.replace("clientLibraries: [java.net.http, com.azure.storage]\n", ""), "clientLibraries",
				"required");
	}

	@Test
	void wrongShapeIsRejected() throws IOException {
		assertRejected(VALID.replace("code: P3", "code: [P3]"), "modules[1].code", "must be a string");
		assertRejected(VALID.replace("published: [api], clientPackages", "published: api, clientPackages"), "modules[1].published",
				"must be a list");
		assertRejected(VALID.replace("published: [api], clientPackages", "published: [7], clientPackages"), "modules[1].published[0]",
				"must be a string");
		assertRejected(VALID.replace("  - { code: P3, name: casewf, published: [api], clientPackages: [] }",
				"  - casewf"), "modules[1]", "must be a mapping");
	}

	@Test
	void emptyPublishedIsRejected() throws IOException {
		assertRejected(VALID.replace("published: [api], clientPackages: []", "published: [], clientPackages: []"),
				"modules[1].published", "required");
		assertRejected(VALID.replace("rootPackage: x.common, published: [api]", "rootPackage: x.common, published: []"),
				"external[0].published", "required");
	}

	@Test
	void emptyModulesIsRejected() throws IOException {
		String noModules = VALID.substring(0, VALID.indexOf("modules:")) + "modules: []\n"
				+ VALID.substring(VALID.indexOf("external:"));
		assertRejected(noModules, "modules", "required");
	}

	@Test
	void duplicateCodeIsRejected() throws IOException {
		assertRejected(VALID.replace("code: P3", "code: P2"), "modules[1].code", "duplicate value P2");
	}

	@Test
	void duplicateNameIsRejected() throws IOException {
		assertRejected(VALID.replace("name: casewf", "name: integration"), "modules[1].name",
				"duplicate value integration");
	}

	@Test
	void badCodePatternIsRejected() throws IOException {
		assertRejected(VALID.replace("code: P3", "code: P11"), "modules[1].code", "does not match");
		assertRejected(VALID.replace("code: P3", "code: S0"), "modules[1].code", "does not match");
	}

	@Test
	void badNamePatternIsRejected() throws IOException {
		assertRejected(VALID.replace("name: casewf", "name: CaseWf"), "modules[1].name", "does not match");
		assertRejected(VALID.replace("name: casewf", "name: case.wf"), "modules[1].name", "does not match");
	}

	@Test
	void badPackagePatternIsRejected() throws IOException {
		assertRejected(VALID.replace("rootPackage: x.recovery", "rootPackage: x..recovery"), "rootPackage",
				"does not match");
		assertRejected(VALID.replace("[api, flags.api]", "[api, Flags.api]"), "modules[0].published[1]",
				"does not match");
		assertRejected(VALID.replace("clientPackages: [adapter]", "clientPackages: [adapter.]"),
				"modules[0].clientPackages[0]", "does not match");
		assertRejected(VALID.replace("rootPackage: x.common", "rootPackage: x/common"), "external[0].rootPackage",
				"does not match");
		assertRejected(VALID.replace("[java.net.http, com.azure.storage]", "[java.net.http, 'com azure']"),
				"clientLibraries[1]", "does not match");
	}

	/** CONF-TE001-01 (spec field matrix: published is unique per module): a repeated entry is refused. */
	@Test
	void duplicatePublishedIsRejected() throws IOException {
		assertRejected(VALID.replace("[api, flags.api]", "[api, flags.api, api]"), "modules[0].published[2]",
				"duplicate value api");
		assertRejected(VALID.replace("rootPackage: x.collection, published: [api]",
				"rootPackage: x.collection, published: [api, api]"), "external[1].published[1]", "duplicate value api");
	}

	@Test
	void internalAsPublishedIsRejected() throws IOException {
		assertRejected(VALID.replace("published: [api], clientPackages", "published: [api, internal], clientPackages"),
				"modules[1].published[1]", "internal");
		assertRejected(VALID.replace("published: [api], clientPackages", "published: [internal.x], clientPackages"),
				"modules[1].published[0]", "internal");
	}

	@Test
	void unknownTopLevelKeyIsRejected() throws IOException {
		assertRejected(VALID + "owner: someone\n", "owner", "unknown key");
	}

	@Test
	void unknownNestedKeyIsRejected() throws IOException {
		assertRejected(VALID.replace("code: P3, ", "code: P3, label: x, "), "modules[1].label", "unknown key");
		assertRejected(VALID.replace("{ name: common, ", "{ name: common, flag: true, "), "external[0].flag",
				"unknown key");
	}

	@Test
	void externalMustBeCommonAndCollection() throws IOException {
		assertRejected(VALID.replace("name: collection", "name: billing"), "external[1].name", "does not match");
		assertRejected(VALID.replace("name: collection", "name: common"), "external[1].name", "duplicate value common");
		assertRejected(VALID.replace("  - { name: collection, rootPackage: x.collection, published: [api] }\n", ""),
				"external", "must list exactly common and collection");
	}

	@Test
	void clientLibrariesMustBeNonEmptyAndUnique() throws IOException {
		assertRejected(VALID.replace("[java.net.http, com.azure.storage]", "[]"), "clientLibraries", "required");
		assertRejected(VALID.replace("[java.net.http, com.azure.storage]", "[java.net.http, java.net.http]"),
				"clientLibraries[1]", "duplicate value java.net.http");
	}

	@Test
	void emptyRequiredStringsAreRejected() throws IOException {
		assertRejected(VALID.replace("rootPackage: x.recovery", "rootPackage: \"\""), "rootPackage", "required");
		assertRejected(VALID.replace("code: P3", "code: \"\""), "modules[1].code", "required");
		assertRejected(VALID.replace("name: casewf", "name: \"\""), "modules[1].name", "required");
		assertRejected(VALID.replace("rootPackage: x.common", "rootPackage: \"\""), "external[0].rootPackage",
				"required");
	}

	@Test
	void wrongListShapeIsRejected() throws IOException {
		assertRejected("rootPackage: x.recovery\nmodules: nope\nclientLibraries: [java.net.http]\n", "modules", "must be a list");
		assertRejected("rootPackage: x.recovery\nmodules:\n  - { code: P3, name: casewf, published: [api], clientPackages: [] }\nexternal: nope\nclientLibraries: [java.net.http]\n", "external", "must be a list");
		assertRejected(VALID.replace("clientLibraries: [java.net.http, com.azure.storage]", "clientLibraries: nope"),
				"clientLibraries", "must be a list");
	}

	@Test
	void missingSectionsAreRejected() throws IOException {
		String withoutExternal = VALID.substring(0, VALID.indexOf("external:")) + "clientLibraries: [java.net.http]\n";
		assertRejected(withoutExternal, "external", "required");
		assertRejected(VALID.replace("clientLibraries: [java.net.http, com.azure.storage]\n", ""), "clientLibraries",
				"required");
	}

	@Test
	void nonStringKeysAndListItemsAreRejected() throws IOException {
		assertRejected(VALID + "1: value\n", "$", "must use string keys");
		assertRejected(VALID.replace("clientPackages: [adapter]", "clientPackages: [7]"),
				"modules[0].clientPackages[0]", "must be a string");
		assertRejected(VALID.replace("published: [api] }", "published: [7] }"), "external[0].published[0]",
				"must be a string");
		assertRejected(VALID.replace("name: casewf", "name: [casewf]"), "modules[1].name", "must be a string");
	}

	@Test
	void clientPackagesMayBeInternal() throws IOException {
		ModuleMap map = ModuleMapLoader.load(
				write(VALID.replace("clientPackages: [adapter]", "clientPackages: [internal]")));

		assertThat(map.modules().getFirst().clientPackages()).containsExactly("internal");
	}

	@Test
	void externalKeysAreRequiredAndUnknownOnesRejected() throws IOException {
		assertRejected(VALID.replace("rootPackage: x.common, ", ""), "external[0].rootPackage", "required");
		assertRejected(VALID.replace("rootPackage: x.common, published: [api]", "rootPackage: x.common"),
				"external[0].published", "required");
	}
}