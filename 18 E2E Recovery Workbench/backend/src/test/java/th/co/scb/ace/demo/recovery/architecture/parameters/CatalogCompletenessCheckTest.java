package th.co.scb.ace.demo.recovery.architecture.parameters;

import static org.assertj.core.api.Assertions.assertThat;

import java.io.IOException;
import java.nio.charset.StandardCharsets;
import java.nio.file.Files;
import java.nio.file.Path;
import java.util.List;

import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.io.TempDir;

/**
 * TC-E1-042-03 (SPEC-RWB-E1-042-003; AC3, BR2, X2): every key read in recovery main code is
 * catalogued, and the reader-call rule refuses the forms that would hide a key from the check.
 */
class CatalogCompletenessCheckTest {

	static final Path MAIN = Path.of("src/main/java");

	static final Path FIXTURE_MAIN = Path.of("src/test/resources/architecture/fixtures/parameter-checks/main");

	static final Path FIXTURES = Path.of("src/test/resources/architecture/fixtures/parameter-checks");

	static final Path CATALOG = Path.of("src/main/resources/config/parameter-catalog.csv");

	private static CatalogFileParser.Result catalog() {
		return CatalogFileParser.parse(CATALOG);
	}

	@Test
	void readsOfAnUncataloguedKeyFail() {
		List<CatalogCompletenessRules.Finding> findings = CatalogCompletenessRules.keyReads(FIXTURE_MAIN, catalog());

		assertThat(findings).filteredOn(finding -> finding.message().contains("allocation.retry.limit")).hasSize(4);
		assertThat(findings).filteredOn(finding -> finding.message().contains("allocation.retry.limit"))
			.allSatisfy(finding -> assertThat(finding.file()).isIn(
					"recovery/casewf/caselist/OtherReads.java", "recovery/dataengine/caselist/ToleranceReader.java"));
	}

	@Test
	void readerCallCases() {
		List<CatalogCompletenessRules.Finding> findings = CatalogCompletenessRules.keyReads(FIXTURE_MAIN, catalog());

		assertThat(findings).anySatisfy(finding -> {
			assertThat(finding.file()).isEqualTo("recovery/dataengine/caselist/ToleranceReader.java");
			assertThat(finding.message()).contains("allocation.retry.limit");
		});
	}

	@Test
	void nonLiteralAndRefusedForms() {
		List<CatalogCompletenessRules.Finding> findings = CatalogCompletenessRules.keyReads(FIXTURE_MAIN, catalog())
			.stream()
			.filter(finding -> finding.file().equals("recovery/dataengine/caselist/ToleranceReader.java"))
			.toList();

		assertThat(findings).anySatisfy(finding -> assertThat(finding.message())
			.contains("first argument is not one string literal"));
		assertThat(findings).anySatisfy(finding -> assertThat(finding.message()).contains("::get is refused"));
		assertThat(findings).anySatisfy(finding -> assertThat(finding.message()).contains("var local"));
		assertThat(findings).allSatisfy(finding -> assertThat(finding.line()).isPositive());
	}

	@Test
	void mapAndOptionalGetAreNotKeyReads(@TempDir Path root) throws IOException {
		Path file = root.resolve("recovery/casewf/caselist/LimitsReader.java");
		Files.createDirectories(file.getParent());
		Files.copy(FIXTURE_MAIN.resolve("recovery/casewf/caselist/LimitsReader.java"), file);

		assertThat(CatalogCompletenessRules.keyReads(root, catalog())).isEmpty();
	}

	@Test
	void exemptImplementationIsSkipped(@TempDir Path root) throws IOException {
		Path file = root.resolve("recovery/casewf/config/CatalogParameterReaderImpl.java");
		Files.createDirectories(file.getParent());
		Files.copy(FIXTURE_MAIN.resolve("recovery/casewf/config/CatalogParameterReaderImpl.java"), file);

		assertThat(CatalogCompletenessRules.keyReads(root, catalog())).isEmpty();
	}

	@Test
	void aCataloguedKeyGivesNoFinding() {
		List<CatalogCompletenessRules.Finding> findings = CatalogCompletenessRules.keyReads(FIXTURE_MAIN, catalog());

		assertThat(findings).noneSatisfy(finding -> assertThat(finding.message()).contains("config.cache.ttl-seconds"));
	}

	@Test
	void theRealMainTreeGivesZeroFindings() {
		assertThat(CatalogCompletenessRules.keyReads(MAIN, catalog())).isEmpty();
	}

	@Test
	void productRowWithoutDefaultPassesAndWithoutOwnerFails() {
		CatalogFileParser.Result passes = CatalogFileParser.parse(FIXTURES.resolve("catalog/product-row.csv"));
		CatalogFileParser.Result fails = CatalogFileParser.parse(FIXTURES.resolve("catalog/product-row-no-owner.csv"));

		assertThat(CatalogCompletenessRules.rowRules(passes)).isEmpty();
		assertThat(CatalogCompletenessRules.rowRules(fails)).anySatisfy(finding ->
				assertThat(finding.message()).contains("owner_role"));
	}

	@Test
	void changedDefaultWithoutMigrationIsReported() {
		CatalogFileParser.Result catalog = catalog();
		CatalogFileParser.Result drift = CatalogFileParser.parse(FIXTURES.resolve("catalog/drift.csv"));
		CatalogRow expected = catalog.rows()
			.stream()
			.filter(row -> row.key().equals("case.entry.dpd"))
			.findFirst()
			.orElseThrow();
		CatalogRow actual = drift.rows()
			.stream()
			.filter(row -> row.key().equals("case.entry.dpd"))
			.findFirst()
			.orElseThrow();

		assertThat(CatalogCompletenessRules.drift(expected, actual)).anySatisfy(finding -> {
			assertThat(finding.file()).isEqualTo("case.entry.dpd");
			assertThat(finding.message()).contains("default_value");
		});
	}

	@Test
	void theCredentialRuleAppliesToEveryEnvRow() {
		CatalogFileParser.Result result = CatalogFileParser.parse(FIXTURES.resolve("catalog/env-credential.csv"));

		assertThat(CatalogCompletenessRules.rowRules(result)).anySatisfy(finding ->
				assertThat(finding.message()).contains("env_property"));
	}

	@Test
	void theRealCatalogIsComplete() {
		assertThat(CatalogCompletenessRules.rowRules(catalog())).isEmpty();
	}

	@Test
	void aFixtureFileIsReadAsUtf8() throws IOException {
		Path file = FIXTURES.resolve("main/recovery/casewf/casecreation/EntryRule.java");

		assertThat(Files.readString(file, StandardCharsets.UTF_8)).contains("int threshold = 90;");
	}
}
