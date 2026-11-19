package th.co.scb.ace.demo.recovery.architecture.codeowners;

import static org.assertj.core.api.Assertions.assertThat;

import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Path;
import java.util.ArrayList;
import java.util.HashSet;
import java.util.List;
import java.util.Map;
import java.util.Set;
import java.util.stream.Stream;

import org.junit.jupiter.api.Tag;
import org.junit.jupiter.api.Test;

/**
 * RWB-TE-002 UT-13..UT-20, UT-25, UT-26 (SPEC-002..-005, -007, -017; AC1..AC4, BR1..BR5, BR7):
 * the ownership resolver on the live {@code .gitlab/CODEOWNERS} and on synthetic fixtures.
 */
@Tag("codeowners")
class OwnershipResolverTest {

	private static final String RECOVERY = "Recovery module";

	private static final String COMMON = "Common module";

	private static final String CONTROL_ACE = "Code owners control ACE team";

	private static final String CONTROL_RECOVERY = "Code owners control recovery";

	private static final String PIPELINE = "Pipeline gates";

	private static final String RECOVERY_TEAM = "@scb-ace/techx-recovery-tech-leads";

	private static final String ACE_TEAM = "@scb-ace/ace-team";

	private static final String PIPELINE_ROLE = "@role-placeholder/techx-devops-with-scb-it";

	private static final String RECOVERY_MAIN = "backend/src/main/java/th/co/scb/ace/demo/recovery/";

	private static final String RECOVERY_TEST = "backend/src/test/java/th/co/scb/ace/demo/recovery/";

	private static final String COMMON_PATH = "backend/src/main/java/th/co/scb/ace/demo/common/ExampleService.java";

	private static final String ALLOCATION = RECOVERY_MAIN + "casewf/internal/AllocationService.java";

	private static final String CODEOWNERS_PACKAGE = RECOVERY_TEST + "architecture/codeowners/";

	private static CodeOwnersFile parse(String... lines) {
		return CodeOwnersFile.parse(List.of(lines));
	}

	private static CodeOwnersFile live() {
		return CodeOwnersFile.parse(CodeOwnersValidator.repositoryRoot().resolve(".gitlab/CODEOWNERS"));
	}

	private static Map<String, Set<String>> resolve(CodeOwnersFile file, String... paths) {
		return OwnershipResolver.resolve(file, List.of(paths));
	}

	private static Set<String> ownersOf(Map<String, Set<String>> result, String section) {
		assertThat(result).containsKey(section);
		return result.get(section);
	}

	@Test
	void specificPatternWinsWithinASection() {
		CodeOwnersFile file = parse("[Recovery module]",
				"/" + RECOVERY_MAIN + " @scb-ace/ace-team",
				"/" + RECOVERY_MAIN + "casewf/ " + RECOVERY_TEAM);

		Map<String, Set<String>> specific = resolve(file, RECOVERY_MAIN + "casewf/CaseFacade.java");
		Map<String, Set<String>> general = resolve(file, RECOVERY_MAIN + "dochub/DocumentStore.java");

		assertThat(ownersOf(specific, RECOVERY)).containsExactly(RECOVERY_TEAM);
		assertThat(specific).hasSize(1);
		assertThat(ownersOf(general, RECOVERY)).containsExactly(ACE_TEAM);
		assertThat(general).hasSize(1);
	}

	@Test
	void recoveryMainPathNeedsRecoveryTeam() {
		Map<String, Set<String>> result = resolve(live(), ALLOCATION);

		assertThat(result).containsOnlyKeys(RECOVERY);
		assertThat(result.get(RECOVERY)).containsExactly(RECOVERY_TEAM);
	}

	@Test
	void recoveryTestE2eMigrationAndModulePathsNeedRecoveryTeam() {
		CodeOwnersFile file = live();
		for (String path : List.of(
				RECOVERY_TEST + "casewf/CaseFacadeTest.java",
				"backend/src/test/java/th/co/scb/ace/demo/e2e/PlatformE2ETest.java",
				"backend/src/main/resources/db/modulemigration/recovery/README.md",
				RECOVERY_MAIN + "dochub/storage/BlobDocumentStore.java",
				RECOVERY_MAIN + "casewf/workflow/internal/TemporalConfig.java",
				RECOVERY_MAIN + "casewf/migration/RecoveryFlywayConfig.java",
				RECOVERY_TEST + "casewf/rules/DroolsRuleEngineTest.java")) {
			Map<String, Set<String>> result = resolve(file, path);

			assertThat(result).as(path).containsOnlyKeys(RECOVERY);
			assertThat(result.get(RECOVERY)).as(path).containsExactly(RECOVERY_TEAM);
		}
	}

	@Test
	void frontendMigrationAndMapPathsNeedRecoveryTeam() {
		CodeOwnersFile file = live();
		for (String path : List.of(
				"frontend/src/modules/recovery/caselist/CaseListPage.tsx",
				"backend/src/main/resources/db/modulemigration/recovery/V9999__rwb_te_002_resolver_fixture.sql",
				"backend/src/test/resources/architecture/recovery-modules.yaml")) {
			Map<String, Set<String>> result = resolve(file, path);

			assertThat(result).as(path).containsOnlyKeys(RECOVERY);
			assertThat(result.get(RECOVERY)).as(path).containsExactly(RECOVERY_TEAM);
		}
	}

	@Test
	void commonModulePathNeedsAceTeam() {
		Map<String, Set<String>> result = resolve(live(), COMMON_PATH);

		assertThat(result).containsOnlyKeys(COMMON);
		assertThat(result.get(COMMON)).containsExactly(ACE_TEAM);
	}

	@Test
	void bothModulesNeedBothTeams() {
		Map<String, Set<String>> result = resolve(live(), ALLOCATION, COMMON_PATH);

		assertThat(result).containsOnlyKeys(COMMON, RECOVERY);
		assertThat(result.get(COMMON)).containsExactly(ACE_TEAM);
		assertThat(result.get(RECOVERY)).containsExactly(RECOVERY_TEAM);
	}

	@Test
	void controlFilesNeedBothTeams() {
		CodeOwnersFile file = live();
		for (String path : List.of(".gitlab/CODEOWNERS", ".gitlab/codeowners-register.yaml",
				".gitlab/host-settings.md")) {
			Map<String, Set<String>> result = resolve(file, path);

			assertThat(result).as(path).containsOnlyKeys(CONTROL_ACE, CONTROL_RECOVERY);
			assertThat(CONTROL_ACE).isNotEqualToIgnoringCase(CONTROL_RECOVERY);
			Set<String> overlap = new HashSet<>(result.get(CONTROL_ACE));
			overlap.retainAll(result.get(CONTROL_RECOVERY));
			assertThat(overlap).as(path).isEmpty();
			assertThat(result.get(CONTROL_ACE)).containsExactly(ACE_TEAM);
			assertThat(result.get(CONTROL_RECOVERY)).containsExactly(RECOVERY_TEAM);
		}

		Map<String, Set<String>> validator = resolve(file, CODEOWNERS_PACKAGE + "CodeOwnersValidator.java");
		assertThat(validator).containsOnlyKeys(RECOVERY, CONTROL_ACE);
		assertThat(validator.get(RECOVERY)).containsExactly(RECOVERY_TEAM);
		assertThat(validator.get(CONTROL_ACE)).containsExactly(ACE_TEAM);
	}

	@Test
	void resolverIsIdempotentAndLeavesUnownedPathsAlone() {
		CodeOwnersFile file = live();

		assertThat(resolve(file, ALLOCATION, COMMON_PATH)).isEqualTo(resolve(file, ALLOCATION, COMMON_PATH));
		assertThat(resolve(file, "README.md")).isEmpty();
		assertThat(resolve(file, ".\\" + ALLOCATION.replace('/', '\\'))).isEqualTo(resolve(file, ALLOCATION));
	}

	@Test
	void pipelineGateFilesNeedThePipelineRole() {
		CodeOwnersFile file = live();
		for (String path : List.of("backend/build.gradle.kts", "backend/settings.gradle.kts",
				"backend/gradle/wrapper/gradle-wrapper.properties", "frontend/package.json",
				"frontend/vite.config.ts", "scripts/dev.ps1")) {
			Map<String, Set<String>> result = resolve(file, path);

			assertThat(result).as(path).containsOnlyKeys(PIPELINE);
			assertThat(result.get(PIPELINE)).as(path).containsExactly(PIPELINE_ROLE);
		}
	}

	@Test
	void addendumPathsHaveOwners() {
		// D-RUN-25 addendum: security review F1, F2 and F4.
		CodeOwnersFile file = live();
		for (String path : List.of("CODEOWNERS", "docs/CODEOWNERS")) {
			Map<String, Set<String>> result = resolve(file, path);

			assertThat(result).as(path).containsOnlyKeys(CONTROL_ACE, CONTROL_RECOVERY);
			assertThat(result.get(CONTROL_ACE)).as(path).containsExactly(ACE_TEAM);
			assertThat(result.get(CONTROL_RECOVERY)).as(path).containsExactly(RECOVERY_TEAM);
		}
		for (String path : List.of("backend/src/main/resources/application.yaml",
				"backend/src/main/resources/application-local.yaml")) {
			Map<String, Set<String>> result = resolve(file, path);

			assertThat(result).as(path).containsOnlyKeys(COMMON, RECOVERY);
			assertThat(result.get(COMMON)).as(path).containsExactly(ACE_TEAM);
			assertThat(result.get(RECOVERY)).as(path).containsExactly(RECOVERY_TEAM);
		}
		for (String path : List.of("backend/Dockerfile", "backend/.dockerignore")) {
			Map<String, Set<String>> result = resolve(file, path);

			assertThat(result).as(path).containsOnlyKeys(PIPELINE);
			assertThat(result.get(PIPELINE)).as(path).containsExactly(PIPELINE_ROLE);
		}
		// REVIEW-001 H4: the access grants, the parameter catalog, the local database build and the
		// migration test fixtures had no owner line.
		for (String path : List.of("backend/src/main/resources/access/interim-capability-grants.csv",
				"backend/src/main/resources/config/parameter-catalog.csv",
				"backend/src/test/resources/migration-lint/t01-name-fail/V0001__rwb_e1_044_ok.sql",
				"backend/src/test/resources/flyway-fixtures/apply-once/V0001__rwb_e1_044_add_queue.sql",
				"infra/postgres/init/20-grants.sql.inc")) {
			Map<String, Set<String>> result = resolve(file, path);

			assertThat(result).as(path).containsOnlyKeys(RECOVERY);
			assertThat(result.get(RECOVERY)).as(path).containsExactly(RECOVERY_TEAM);
		}
	}

	@Test
	void everyRecoveryTestFileResolvesToTheRecoveryTeam() throws IOException {
		Path root = CodeOwnersValidator.repositoryRoot();
		CodeOwnersFile file = live();

		// (A) the RWB-TE-001 boundary controls
		for (String path : List.of(RECOVERY_TEST + "architecture/RecoveryBoundaryTest.java",
				"backend/src/test/java/th/co/scb/ace/demo/ModulithTest.java",
				"backend/src/test/resources/architecture/recovery-modules.yaml")) {
			assertThat(resolve(file, path).get(RECOVERY)).as(path).containsExactly(RECOVERY_TEAM);
		}

		// (B) every regular file under test resources/architecture and test java, except the common test folder
		List<String> scanned = new ArrayList<>();
		scanned.addAll(regularFiles(root, "backend/src/test/resources/architecture"));
		scanned.addAll(regularFiles(root, "backend/src/test/java").stream()
			.filter(path -> !path.startsWith("backend/src/test/java/th/co/scb/ace/demo/common/"))
			.toList());
		List<String> unowned = new ArrayList<>();
		for (String path : scanned) {
			Map<String, Set<String>> result = resolve(file, path);
			if (result.get(RECOVERY) == null || !result.get(RECOVERY).equals(Set.of(RECOVERY_TEAM))) {
				unowned.add(path);
			}
			if (path.startsWith(CODEOWNERS_PACKAGE)) {
				assertThat(result.get(CONTROL_ACE)).as(path).containsExactly(ACE_TEAM);
			}
		}
		assertThat(unowned).as("files without [Recovery module] -> " + RECOVERY_TEAM).isEmpty();
		assertThat(scanned).anyMatch(path -> path.startsWith("backend/src/test/resources/architecture/fixtures/"));
		assertThat(scanned).anyMatch(path -> path.startsWith("backend/src/test/java/th/co/scb/ace/boundaryfixture/"));

		// (C) the D-RCV-39 frontend import rule file
		Map<String, Set<String>> eslint = resolve(file, "frontend/eslint.config.js");
		assertThat(eslint).containsOnlyKeys(RECOVERY, PIPELINE);
		assertThat(eslint.get(RECOVERY)).containsExactly(RECOVERY_TEAM);
		assertThat(eslint.get(PIPELINE)).containsExactly(PIPELINE_ROLE);

		assertThat(Files.readString(root.resolve(".gitlab/CODEOWNERS"))).doesNotContain("{te001FixtureRoot}");
	}

	private static List<String> regularFiles(Path root, String folder) throws IOException {
		try (Stream<Path> files = Files.walk(root.resolve(folder))) {
			return files.filter(Files::isRegularFile)
				.map(path -> root.relativize(path).toString().replace('\\', '/'))
				.sorted()
				.toList();
		}
	}
}
