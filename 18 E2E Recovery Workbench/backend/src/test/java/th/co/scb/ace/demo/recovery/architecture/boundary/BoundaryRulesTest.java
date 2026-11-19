package th.co.scb.ace.demo.recovery.architecture.boundary;

import static org.assertj.core.api.Assertions.assertThat;

import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Path;
import java.util.ArrayList;
import java.util.List;
import java.util.stream.Stream;

import com.tngtech.archunit.core.domain.JavaClass;
import com.tngtech.archunit.core.domain.JavaClasses;
import com.tngtech.archunit.core.importer.ClassFileImporter;
import com.tngtech.archunit.lang.ArchRule;
import com.tngtech.archunit.lang.EvaluationResult;
import org.junit.jupiter.api.Test;

/**
 * RWB-TE-001 T-TE001-02..-04, -09, -15 (SPEC-004..-010, BR1..BR6): every rule of the map-driven
 * boundary test fails on its breaking fixture world and passes on its passing fixture world.
 */
class BoundaryRulesTest {

	private static final Path FIXTURES = Path.of("src/test/resources/architecture/fixtures");

	private static final Path TOOLING = Path.of("src/test/java/th/co/scb/ace/demo/recovery/architecture/boundary");

	private static final String FIXTURE_ROOT = "th.co.scb.ace.boundaryfixture";

	private static final String TOOLING_PACKAGE_LITERAL = "th.co.scb.ace.demo.recovery";

	private static ModuleMap map(String name) {
		return ModuleMapLoader.load(FIXTURES.resolve(name));
	}

	private static JavaClasses classes(String world) {
		return new ClassFileImporter().importPackages(FIXTURE_ROOT + "." + world);
	}

	private static List<String> violations(ArchRule rule, String world) {
		EvaluationResult result = rule.evaluate(classes(world));
		return result.getFailureReport().getDetails();
	}

	private static String line(String code, String origin, String dependency, String module) {
		return "Rule " + code + " broken: " + origin + " depends on " + dependency + ". Use " + module
				+ ".api or an application event.";
	}

	@Test
	void collectionInternalDependencyBreaksBnd1() {
		List<String> lines = violations(BoundaryRules.bnd1(map("bnd1.yaml")), "bnd1");

		assertThat(lines).containsExactlyInAnyOrder(
				line("BND-1", "th.co.scb.ace.boundaryfixture.bnd1.recovery.casewf.internal.SampleService",
						"th.co.scb.ace.boundaryfixture.bnd1.collection.internal.CollectorRepository", "collection"),
				line("BND-1", "th.co.scb.ace.boundaryfixture.bnd1.recovery.casewf.internal.SampleReport",
						"th.co.scb.ace.boundaryfixture.bnd1.collection.internal.CollectorRepository", "collection"));
	}

	@Test
	void allViolationsOfARuleInOneRun() {
		EvaluationResult result = BoundaryRules.bnd1(map("bnd1.yaml")).evaluate(classes("bnd1"));

		assertThat(result.hasViolation()).isTrue();
		assertThat(result.getFailureReport().getDetails()).hasSize(2);
	}

	@Test
	void commonInternalDependencyBreaksBnd2() {
		List<String> lines = violations(BoundaryRules.bnd2(map("bnd2.yaml")), "bnd2");

		assertThat(lines).containsExactlyInAnyOrder(
				line("BND-2", "th.co.scb.ace.boundaryfixture.bnd2.recovery.casewf.internal.SampleService",
						"th.co.scb.ace.boundaryfixture.bnd2.common.internal.CustomerCache", "common"),
				line("BND-2", "th.co.scb.ace.boundaryfixture.bnd2.recovery.casewf.internal.SampleSecretReader",
						"th.co.scb.ace.boundaryfixture.bnd2.common.api.internal.SecretHelper", "common"));
	}

	@Test
	void publishedCommonPackageItselfIsAllowed() {
		List<String> lines = violations(BoundaryRules.bnd2(map("bnd2.yaml")), "bnd2");

		assertThat(lines).noneSatisfy(text -> assertThat(text).contains("SampleLookupUser"));
	}

	@Test
	void commonApiDependencyPassesEveryRule() {
		ModuleMap map = map("passing.yaml");
		for (ArchRule rule : BoundaryRules.all(map)) {
			assertThat(violations(rule, "passing")).as(rule.toString()).isEmpty();
		}
	}

	@Test
	void mapRuleAcceptsPackagePrivateBaseTypeAndUnlistedSubPackage() {
		JavaClasses passing = classes("passing");

		assertThat(violations(BoundaryRules.moduleMap(map("passing.yaml")), "passing")).isEmpty();
		assertThat(passing.stream().map(JavaClass::getName)).contains(
				"th.co.scb.ace.boundaryfixture.passing.recovery.casewf.CaseModuleSupport",
				"th.co.scb.ace.boundaryfixture.passing.recovery.casewf.workflow.internal.WorkflowRunner");
	}

	@Test
	void publishedWriterMatchesTheFixtureMap() {
		assertThat(violations(BoundaryRules.moduleMap(map("bnd3pass.yaml")), "bnd3pass")).isEmpty();
	}

	@Test
	void foreignEntityAndRepositoryBreakBnd4() {
		List<String> lines = violations(BoundaryRules.bnd4(map("bnd4.yaml")), "bnd4");

		assertThat(lines).containsExactlyInAnyOrder(
				line("BND-4", "th.co.scb.ace.boundaryfixture.bnd4.recovery.integration.internal.CaseExportJob",
						"th.co.scb.ace.boundaryfixture.bnd4.recovery.casewf.internal.RecoveryCaseEntity", "casewf"),
				line("BND-4", "th.co.scb.ace.boundaryfixture.bnd4.recovery.integration.internal.CaseExportJob",
						"th.co.scb.ace.boundaryfixture.bnd4.recovery.casewf.internal.RecoveryCaseRepository", "casewf"),
				line("BND-4", "th.co.scb.ace.boundaryfixture.bnd4.recovery.integration.internal.LegacyLoanReader",
						"th.co.scb.ace.boundaryfixture.bnd4.collection.internal.CollectorEntity", "collection"),
				line("BND-4", "th.co.scb.ace.boundaryfixture.bnd4.recovery.integration.internal.ArchiveReader",
						"th.co.scb.ace.boundaryfixture.bnd4.legacy.ArchivedLoanEntity",
						"th.co.scb.ace.boundaryfixture.bnd4.legacy"));
	}

	@Test
	void clientLibraryOutsideClientPackageBreaksBnd5() {
		List<String> lines = violations(BoundaryRules.bnd5(map("bnd5.yaml")), "bnd5");

		assertThat(lines).containsExactlyInAnyOrder(
				line("BND-5", "th.co.scb.ace.boundaryfixture.bnd5.recovery.casewf.internal.SampleService",
						"java.net.http.HttpClient", "integration"),
				line("BND-5", "th.co.scb.ace.boundaryfixture.bnd5.recovery.casewf.internal.BlobUser",
						"com.azure.storage.blob.BlobClient", "integration"),
				line("BND-5", "th.co.scb.ace.boundaryfixture.bnd5.recovery.casewf.internal.UrlHelper", "java.net.URL",
						"integration"),
				line("BND-5", "th.co.scb.ace.boundaryfixture.bnd5.recovery.casewf.internal.VendorUser",
						"th.co.scb.ace.boundaryfixture.bnd5.vendor.VendorClient$Session", "integration"));
		assertThat(lines).allSatisfy(text -> assertThat(text).endsWith("Use integration.api or an application event."));
	}

	@Test
	void bnd5TextWithoutP2UsesTheOriginModule() {
		List<String> lines = violations(BoundaryRules.bnd5(map("bnd5-nop2.yaml")), "bnd5");

		assertThat(lines).containsExactlyInAnyOrder(
				line("BND-5", "th.co.scb.ace.boundaryfixture.bnd5.recovery.casewf.internal.SampleService",
						"java.net.http.HttpClient", "casewf"),
				line("BND-5", "th.co.scb.ace.boundaryfixture.bnd5.recovery.casewf.internal.BlobUser",
						"com.azure.storage.blob.BlobClient", "casewf"),
				line("BND-5", "th.co.scb.ace.boundaryfixture.bnd5.recovery.casewf.internal.UrlHelper", "java.net.URL",
						"casewf"),
				line("BND-5", "th.co.scb.ace.boundaryfixture.bnd5.recovery.casewf.internal.VendorUser",
						"th.co.scb.ace.boundaryfixture.bnd5.vendor.VendorClient$Session", "casewf"),
				line("BND-5", "th.co.scb.ace.boundaryfixture.bnd5.recovery.integration.adapter.PartnerHttpAdapter",
						"java.net.http.HttpClient",
						"th.co.scb.ace.boundaryfixture.bnd5.recovery.integration.adapter"),
				line("BND-5", "th.co.scb.ace.boundaryfixture.bnd5.recovery.integration.adapter.PartnerHttpAdapter",
						"com.azure.storage.blob.BlobClient",
						"th.co.scb.ace.boundaryfixture.bnd5.recovery.integration.adapter"));
	}

	@Test
	void clientLibraryMatchesOnANameBoundary() {
		List<String> lines = violations(BoundaryRules.bnd5(map("bnd5.yaml")), "bnd5");

		assertThat(lines).anySatisfy(text -> assertThat(text).contains("UrlHelper depends on java.net.URL."));
		assertThat(lines).anySatisfy(
				text -> assertThat(text).contains("VendorUser depends on th.co.scb.ace.boundaryfixture.bnd5.vendor.VendorClient$Session."));
		assertThat(lines).noneSatisfy(text -> assertThat(text).contains("URLEncoder"));
		assertThat(lines).noneSatisfy(text -> assertThat(text).contains("SocketTimeoutException"));
		assertThat(lines).noneSatisfy(text -> assertThat(text).contains("java.net.URI"));
	}

	@Test
	void matchesClientLibraryTable() {
		assertThat(BoundaryRules.matchesClientLibrary("java.net.URL", "java.net.URL")).isTrue();
		assertThat(BoundaryRules.matchesClientLibrary("java.net.URL", "java.net.URLEncoder")).isFalse();
		assertThat(BoundaryRules.matchesClientLibrary("java.net.http", "java.net.http.HttpClient")).isTrue();
		assertThat(BoundaryRules.matchesClientLibrary("java.net.http", "java.net.HttpURLConnection")).isFalse();
		assertThat(BoundaryRules.matchesClientLibrary("com.azure.storage", "com.azure.storage.blob.BlobClient"))
			.isTrue();
		assertThat(BoundaryRules.matchesClientLibrary("th.co.scb.ace.boundaryfixture.bnd5.vendor.VendorClient",
				"th.co.scb.ace.boundaryfixture.bnd5.vendor.VendorClient$Session"))
			.isTrue();
		assertThat(BoundaryRules.matchesClientLibrary("java.net.Socket", "java.net.SocketTimeoutException")).isFalse();
	}

	@Test
	void packageMissingFromTheMapFails() {
		List<String> lines = violations(BoundaryRules.moduleMap(map("vendorx.yaml")), "vendorx");

		assertThat(lines).containsExactly(
				"package th.co.scb.ace.boundaryfixture.vendorx.recovery.vendorx is not in the module map");
	}

	@Test
	void emptyExternalRootsPass() {
		ModuleMap map = map("vendorx.yaml");

		assertThat(violations(BoundaryRules.bnd1(map), "vendorx")).isEmpty();
		assertThat(violations(BoundaryRules.bnd2(map), "vendorx")).isEmpty();
	}

	@Test
	void mapViolationsAreAllReported() {
		List<String> lines = violations(BoundaryRules.moduleMap(map("mapbad.yaml")), "mapbad");

		assertThat(lines).containsExactlyInAnyOrder(
				"module payments (P8) in the module map has no package th.co.scb.ace.boundaryfixture.mapbad.recovery.payments",
				"type th.co.scb.ace.boundaryfixture.mapbad.recovery.RootHelper in root package th.co.scb.ace.boundaryfixture.mapbad.recovery; only package-info is allowed",
				"package th.co.scb.ace.boundaryfixture.mapbad.recovery.casewf.spi has @NamedInterface but is not in the published list of module casewf",
				"published package th.co.scb.ace.boundaryfixture.mapbad.recovery.casewf.events of module casewf has no @NamedInterface",
				"package th.co.scb.ace.boundaryfixture.mapbad.recovery.tools is not in the module map",
				"public type th.co.scb.ace.boundaryfixture.mapbad.recovery.casewf.CaseFacade in module base package th.co.scb.ace.boundaryfixture.mapbad.recovery.casewf; move it to a published package or internal",
				"type-level @NamedInterface on th.co.scb.ace.boundaryfixture.mapbad.recovery.casewf.internal.ExposedHelper; declare published packages in package-info and the module map",
				"@NamedInterface on th.co.scb.ace.boundaryfixture.mapbad.recovery.casewf.timers must declare propagate = false; list each published sub-package in the module map");
	}

	@Test
	void toolingHoldsNoRecoveryPackageLiteral() throws IOException {
		List<String> offenders = new ArrayList<>();
		try (Stream<Path> files = Files.list(TOOLING)) {
			for (Path file : files.filter(path -> path.toString().endsWith(".java"))
				.filter(path -> !path.toString().endsWith("Test.java"))
				.toList()) {
				for (String found : recoveryLiterals(Files.readString(file))) {
					offenders.add(file.getFileName() + ": " + found);
				}
			}
		}

		assertThat(offenders).as("BR6: the tooling reads the root package from the map").isEmpty();
	}

	@Test
	void packageLiteralScanSeesLiteralsOnly() {
		String sample = """
				package %1$s.casewf;
				import %1$s.casewf.RuleInput;
				// %1$s.casewf in a comment is not a literal
				class Sample {
					String name() {
						return "%1$s.casewf";
					}
				}
				""".formatted(TOOLING_PACKAGE_LITERAL);

		assertThat(recoveryLiterals(sample))
			.containsExactly("return \"th.co.scb.ace.demo.recovery.casewf\";");
		assertThat(recoveryLiterals("package th.co.scb.ace.demo.recovery.x;\nimport th.co.scb.ace.demo.recovery.y.Z;\n"))
			.isEmpty();
	}

	private static List<String> recoveryLiterals(String source) {
		List<String> found = new ArrayList<>();
		for (String line : source.split("\\R")) {
			String trimmed = line.trim();
			if (trimmed.startsWith("package ") || trimmed.startsWith("import ") || trimmed.startsWith("//")
					|| trimmed.startsWith("*") || trimmed.startsWith("/*")) {
				continue;
			}
			if (line.contains(TOOLING_PACKAGE_LITERAL)) {
				found.add(trimmed);
			}
		}
		return found;
	}
}
