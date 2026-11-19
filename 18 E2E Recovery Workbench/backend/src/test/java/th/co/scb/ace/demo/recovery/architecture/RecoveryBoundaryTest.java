package th.co.scb.ace.demo.recovery.architecture;

import static com.tngtech.archunit.lang.syntax.ArchRuleDefinition.noClasses;
import static org.assertj.core.api.Assertions.assertThat;

import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Path;
import java.util.ArrayList;
import java.util.List;
import java.util.Map;
import java.util.Set;
import java.util.TreeMap;
import java.util.regex.Pattern;
import java.util.stream.Collectors;
import java.util.stream.Stream;

import com.tngtech.archunit.core.domain.JavaClass;
import com.tngtech.archunit.core.domain.JavaClasses;
import com.tngtech.archunit.core.domain.JavaModifier;
import com.tngtech.archunit.core.importer.ClassFileImporter;
import com.tngtech.archunit.core.importer.ImportOption;
import com.tngtech.archunit.lang.ArchRule;
import org.junit.jupiter.api.Test;
import org.springframework.modulith.core.ApplicationModule;
import org.springframework.modulith.core.ApplicationModules;
import org.springframework.modulith.core.NamedInterface;

import th.co.scb.ace.demo.AceRecoveryApplication;
import th.co.scb.ace.demo.recovery.architecture.boundary.BoundaryRules;
import th.co.scb.ace.demo.recovery.architecture.boundary.ModuleMap;
import th.co.scb.ace.demo.recovery.architecture.boundary.ModuleMapLoader;

/**
 * Recovery boundary rules that Spring Modulith does not cover (RWB-TE-001 SPEC-004..-010, -025,
 * -026). The rules read the module map; the published surface and package skeleton are asserted
 * against the real main classes.
 */
class RecoveryBoundaryTest {

	private static final ModuleMap MAP = ModuleMapLoader
		.load(Path.of("src/test/resources/architecture/recovery-modules.yaml"));

	private static final Path SOURCES = Path
		.of("src/main/java", MAP.rootPackage().replace('.', '/'));

	private static final Set<String> PUBLISHED_PACKAGES = MAP.modules()
		.stream()
		.flatMap(module -> module.published().stream().map(entry -> module.name() + "." + entry))
		.collect(Collectors.toUnmodifiableSet());

	private final JavaClasses classes = new ClassFileImporter()
		.withImportOption(ImportOption.Predefined.DO_NOT_INCLUDE_TESTS)
		.importPackages(MAP.rootPackage());

	/** MAP: every package, published package and module base package agrees with the map (SPEC-004). */
	@Test
	void moduleMapRule() {
		BoundaryRules.moduleMap(MAP).check(classes);
	}

	/** BND-1: no recovery class uses a collection class outside its published packages (SPEC-005). */
	@Test
	void bnd1CollectionBoundary() {
		BoundaryRules.bnd1(MAP).check(classes);
	}

	/** BND-2: no recovery class uses a common class outside its published packages (SPEC-006). */
	@Test
	void bnd2CommonBoundary() {
		BoundaryRules.bnd2(MAP).check(classes);
	}

	/** BND-4: an entity or repository is used only inside its own module (SPEC-008). */
	@Test
	void bnd4EntitiesAndRepositoriesStayInTheirModule() {
		BoundaryRules.bnd4(MAP).check(classes);
	}

	/** BND-5: client libraries only in the using module's client packages (SPEC-009). */
	@Test
	void bnd5ClientLibrariesOnlyInClientPackages() {
		BoundaryRules.bnd5(MAP).check(classes);
	}

	/** SPEC-001 (b), SPEC-025: every map module has the base, api and internal package-info. */
	@Test
	void everyMapModuleHasApiAndInternalPackageInfo() throws IOException {
		for (ModuleMap.Module module : MAP.modules()) {
			Path base = SOURCES.resolve(module.name());
			assertThat(base.resolve("package-info.java")).as(module.name() + " base package-info").exists();
			assertThat(base.resolve("api").resolve("package-info.java")).as(module.name() + " api package-info")
				.exists();
			assertThat(base.resolve("internal").resolve("package-info.java"))
				.as(module.name() + " internal package-info")
				.exists();
			assertThat(Files.readString(base.resolve("package-info.java")))
				.as(module.name() + " @ApplicationModule")
				.contains("@org.springframework.modulith.ApplicationModule");
			assertThat(Files.readString(base.resolve("api").resolve("package-info.java")))
				.as(module.name() + " @NamedInterface")
				.contains("@org.springframework.modulith.NamedInterface(name = \"api\", propagate = false)");
		}
	}

	/** T-TE001-14 (SPEC-025): the public surface of every published package is exactly the map. */
	@Test
	void publishedSurfaceIsExactlyTheSpecifiedTypes() {
		// Candidates come from the map (BR6): the test compares the exact public types of every package
		// the map publishes, so a new public type in a published package fails the comparison below.
		// Packages the map does not publish are skipped here; a public type in one of them is caught by
		// BND-1/BND-2, Modulith verify and the module-map rule when another module uses it
		// (CONF-TE001-02). The seven type-bearing packages are asserted so a map that loses one fails
		// here with a clear message.
		assertThat(PUBLISHED_PACKAGES).as("the map lists the packages that hold published types")
			.contains("casewf.config.api", "casewf.rules", "casewf.timers", "casewf.workflow",
					"integration.flags.api", "access.api", "dochub.api");
		Map<String, List<String>> actual = new TreeMap<>();
		for (JavaClass type : classes) {
			String packageName = type.getPackageName();
			if (!packageName.startsWith(MAP.rootPackage() + ".")) {
				continue;
			}
			String relative = packageName.substring(MAP.rootPackage().length() + 1);
			if (!PUBLISHED_PACKAGES.contains(relative) || !type.getModifiers().contains(JavaModifier.PUBLIC)) {
				continue;
			}
			actual.computeIfAbsent(relative, key -> new ArrayList<>())
				.add(type.getName().substring(packageName.length() + 1));
		}
		actual.values().forEach(types -> types.sort(String::compareTo));

		assertThat(actual).containsExactlyInAnyOrderEntriesOf(Map.of(
				"casewf.rules", List.of("CompiledRulePackage", "RuleEngine", "RuleEngine$RuleCompilationException",
						"RuleInput", "RuleOutcome", "RuleResult"),
				"casewf.timers", List.of("TimerScheduler", "TimerScheduler$TimerDue"),
				"casewf.workflow", List.of("WorkflowIds"),
				"integration.flags.api", List.of("RecoveryFlags"),
				"access.api", List.of("ApiError", "ApiProblemException", "CapabilityCheck", "CatalogParameterReader",
						"CatalogParameterReader$Value", "MessageResolver"),
				"casewf.config.api", List.of("BusinessDateProvider", "CatalogEntry", "ParameterKey", "ParameterKeys",
						"ParameterLoadHandler", "ParameterLoadResult", "ParameterNotInForceException",
						"ParameterService", "ParameterValue", "ParameterVersionApproved",
						"ParameterVersionApproved$Version", "SecretNotServedException"),
				"dochub.api", List.of("DocumentStore", "DocumentStore$DocumentImmutableException",
						"DocumentStore$StoredDocument")));
	}

	/** T-TE001-14 (SPEC-025): the casewf named interfaces are the published packages only. */
	@Test
	void casewfNamedInterfacesAreTheSpecifiedBoundedSet() throws IOException {
		ApplicationModules modules = ApplicationModules.of(AceRecoveryApplication.class);
		ApplicationModule casewf = modules.stream()
			.filter(module -> module.getBasePackage().getName().equals(MAP.rootPackage() + ".casewf"))
			.findFirst()
			.orElseThrow();
		List<NamedInterface> named = casewf.getNamedInterfaces()
			.stream()
			.filter(interfaces -> !interfaces.isUnnamed())
			.toList();

		assertThat(named).allMatch(interfaces -> Set.of("api", "config.api", "rules", "timers", "workflow")
			.contains(interfaces.getName()));
		assertThat(named).extracting(NamedInterface::getName).contains("api", "rules", "timers", "workflow");
		assertThat(named).allSatisfy(interfaces -> assertThat(interfaces.asJavaClasses()
			.map(JavaClass::getPackageName)
			.toList()).allMatch(packageName -> !packageName.endsWith(".internal")));
		// Spring Modulith 2.1 surfaces the named interfaces of a module's direct sub-packages only, so
		// the nested casewf.config.api is asserted from the module map (the only source of published
		// packages, BR6) and from its package-info, which holds the annotation itself.
		ModuleMap.Module casewfModule = MAP.modules()
			.stream()
			.filter(module -> module.name().equals("casewf"))
			.findFirst()
			.orElseThrow();
		assertThat(casewfModule.published()).contains("config.api");
		String nested = Files.readString(SOURCES.resolve("casewf/config/api/package-info.java"));
		assertThat(nested).contains("@org.springframework.modulith.NamedInterface(name = \"config.api\", propagate = false)");
	}

	/** BS-6.1: workflow code is deterministic; clock, random and I/O are activity work. */
	@Test
	void workflowImplementationsAreDeterministic() {
		ArchRule rule = noClasses()
				.that().resideInAPackage(MAP.rootPackage() + ".casewf.workflow..")
				.and().haveSimpleNameEndingWith("Impl")
				.should().callMethod(System.class, "currentTimeMillis")
				.orShould().callMethod(java.time.Instant.class, "now")
				.orShould().callMethod(java.time.LocalDateTime.class, "now")
				.orShould().callMethod(java.time.LocalDate.class, "now")
				.orShould().callMethod(java.util.UUID.class, "randomUUID")
				.orShould().dependOnClassesThat().resideInAnyPackage("java.util.random..", "java.io..", "java.net..",
						"java.sql..", "javax.sql..", "org.springframework.jdbc..", "java.nio.file..")
				.orShould().dependOnClassesThat().areAssignableTo(java.util.Random.class)
				.orShould().dependOnClassesThat().areAssignableTo(Thread.class)
				.allowEmptyShould(true);
		rule.check(classes);
	}

	/** SPEC-026: the retargeted determinism rule selects the smoke workflow implementation. */
	@Test
	void determinismRuleSelectsTheSmokeWorkflowImpl() {
		List<String> impls = classes.stream()
			.filter(type -> type.getPackageName().startsWith(MAP.rootPackage() + ".casewf.workflow"))
			.filter(type -> type.getSimpleName().endsWith("Impl"))
			.map(JavaClass::getName)
			.toList();

		assertThat(impls).contains("th.co.scb.ace.demo.recovery.casewf.workflow.internal.PlatformSmokeWorkflow$Impl");
	}

	/** BND-6: a recovery class may not name an ACE public table; read recovery.v_ace_* instead. */
	@Test
	void noRecoveryClassNamesAPublicTable() throws IOException {
		Pattern publicTable = Pattern.compile("(?i)\\bpublic\\.[a-z_][a-z0-9_]*");
		List<String> offenders;
		try (Stream<Path> files = Files.walk(SOURCES)) {
			offenders = files.filter(p -> p.toString().endsWith(".java")).flatMap(p -> {
				try {
					return Files.readAllLines(p).stream()
							.filter(line -> !line.trim().startsWith("*") && !line.trim().startsWith("//"))
							.filter(line -> publicTable.matcher(line).find())
							.map(line -> SOURCES.relativize(p) + ": " + line.trim());
				}
				catch (IOException ex) {
					throw new IllegalStateException(ex);
				}
			}).toList();
		}
		assertThat(offenders).as("BND-6: read ACE data through recovery.v_ace_* views").isEmpty();
	}
}
