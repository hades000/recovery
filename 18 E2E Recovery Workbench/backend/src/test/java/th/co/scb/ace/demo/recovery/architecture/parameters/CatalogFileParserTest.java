package th.co.scb.ace.demo.recovery.architecture.parameters;

import static org.assertj.core.api.Assertions.assertThat;

import java.nio.file.Path;
import java.util.List;
import java.util.Map;
import java.util.stream.Collectors;

import org.junit.jupiter.api.Test;

/**
 * TC-E1-042-41 and TC-E1-042-44 (SPEC-RWB-E1-042-003, -005; BR2, BR6): the catalog file parses, the
 * {@code used_by} grammar holds and no ENV row names a credential-bearing property.
 */
class CatalogFileParserTest {

	static final Path CATALOG = Path.of("src/main/resources/config/parameter-catalog.csv");

	static final Path FIXTURES = Path.of("src/test/resources/architecture/fixtures/parameter-checks/catalog");

	/** Builds one catalog row; the 16 columns of §7.1 in order. */
	static String row(String key, String kind, String type, String unit, String min, String max, String dflt,
			String scope, boolean required, String owner, String environments, String usedBy, boolean secret,
			String valueSource, String envProperty, String description) {
		return String.join(",", key, kind, type, unit, min, max, dflt, scope, String.valueOf(required), owner,
				environments, usedBy, String.valueOf(secret), valueSource, envProperty, description);
	}

	@Test
	void realCatalogParsesAndUsedBySplits() {
		CatalogFileParser.Result result = CatalogFileParser.parse(CATALOG);

		assertThat(result.findings()).as("catalog findings").isEmpty();
		assertThat(result.rows()).hasSize(19);

		Map<String, List<String>> usedBy = result.rows()
			.stream()
			.collect(Collectors.toMap(CatalogRow::key, CatalogRow::usedBy));
		assertThat(usedBy.get("case.entry.dpd")).containsExactly("recovery.casewf.casecreation");
		assertThat(usedBy.get("temporal.retention.days")).containsExactly(
				"recovery.casewf.workflow (RWB-E1-070, RWB-E1-071)", "RWB-E2-039");
		assertThat(usedBy.get("ENTRY_DPD")).containsExactly("recovery.casewf.casecreation",
				"recovery.casewf.allocation");
		assertThat(usedBy.get("EXPOSURE_BAND_SET")).containsExactly("recovery.casewf.allocation");
		assertThat(usedBy.get("rules.testcases.min")).containsExactly("RWB-E1-073");
		assertThat(usedBy.get("ace.db.password")).containsExactly("ACE common module");
		assertThat(result.rows()).allSatisfy(catalogRow -> assertThat(catalogRow.environments())
			.containsExactly("DEV", "SIT", "UAT", "PROD"));
		assertThat(result.rows()).filteredOn(CatalogRow::secret).extracting(CatalogRow::key)
			.containsExactly("ace.db.password");
	}

	@Test
	void usedByGrammarRejectsBrokenValues() {
		CatalogFileParser.Result result = CatalogFileParser.parse(FIXTURES.resolve("used-by-broken.csv"));

		assertThat(result.findings()).isNotEmpty();
		assertThat(result.findings()).allSatisfy(finding -> assertThat(finding.column()).isEqualTo("used_by"));
		assertThat(result.findings()).extracting(CatalogFileParser.CatalogFinding::key)
			.containsExactlyInAnyOrder("u1", "u2", "u3", "u4", "u5", "u6");
	}

	@Test
	void credentialBearingPropertiesAreRefused() {
		CatalogFileParser.Result result = CatalogFileParser.parse(FIXTURES.resolve("env-credential.csv"));

		assertThat(result.findings()).extracting(CatalogFileParser.CatalogFinding::key)
			.containsExactlyInAnyOrder("c1", "c2", "c3", "c4", "c5", "c6", "c7", "c8", "c9", "c10", "c11");
		assertThat(result.findings()).allSatisfy(finding -> assertThat(finding.column()).isEqualTo("env_property"));
		assertThat(result.rows()).extracting(CatalogRow::key).contains("ok1", "ok2");
	}

	@Test
	void aWrongHeaderFailsNamingTheColumn() {
		CatalogFileParser.Result result = CatalogFileParser.parse("key,kind,value_type\nx,BUSINESS,STRING\n");

		assertThat(result.findings()).extracting(CatalogFileParser.CatalogFinding::column).containsExactly("header");
	}

	@Test
	void aDuplicateKeyFails() {
		String dup = row("dup", "BUSINESS", "STRING", "", "", "", "x", "GLOBAL", false, "RW-COE", "DEV", "SOMEWHERE",
				false, "TABLE", "", "A description.");

		CatalogFileParser.Result result = CatalogFileParser.parse(
				CatalogFileParser.HEADER + "\n" + dup + "\n" + dup + "\n");

		assertThat(result.findings()).extracting(CatalogFileParser.CatalogFinding::column).contains("key");
	}

	@Test
	void aMissingDefaultFailsUnlessProductSecretOrEnv() {
		CatalogFileParser.Result result = CatalogFileParser.parse(CatalogFileParser.HEADER + "\n"
				+ row("d1", "BUSINESS", "STRING", "", "", "", "", "GLOBAL", false, "RW-COE", "DEV", "SOMEWHERE", false,
						"TABLE", "", "A description.")
				+ "\n"
				+ row("d2", "BUSINESS", "STRING", "", "", "", "", "PRODUCT", false, "RW-COE", "DEV", "SOMEWHERE", false,
						"TABLE", "", "A description.")
				+ "\n"
				+ row("d3", "ENVIRONMENT", "STRING", "", "", "", "", "GLOBAL", false, "RW-COE", "DEV", "SOMEWHERE", true,
						"SECRET", "", "A description.")
				+ "\n"
				+ row("d4", "ENVIRONMENT", "STRING", "", "", "", "", "GLOBAL", false, "RW-COE", "DEV", "SOMEWHERE", false,
						"ENV", "rwb.some.property", "A description.")
				+ "\n");

		assertThat(result.findings()).extracting(CatalogFileParser.CatalogFinding::key).containsExactly("d1");
	}

	@Test
	void aDefaultOutsideItsRangeFails() {
		String outOfRange = row("r1", "BUSINESS", "INTEGER", "DAYS", "1", "10", "11", "GLOBAL", false, "RW-COE", "DEV",
				"SOMEWHERE", false, "TABLE", "", "A description.");

		CatalogFileParser.Result result = CatalogFileParser.parse(
				CatalogFileParser.HEADER + "\n" + outOfRange + "\n");

		assertThat(result.findings()).extracting(CatalogFileParser.CatalogFinding::column)
			.containsExactly("default_value");
	}

	@Test
	void anEnvRowWithoutAPropertyFails() {
		String noProperty = row("e1", "ENVIRONMENT", "STRING", "", "", "", "x", "GLOBAL", false, "RW-COE", "DEV",
				"SOMEWHERE", false, "ENV", "", "A description.");

		CatalogFileParser.Result result = CatalogFileParser.parse(
				CatalogFileParser.HEADER + "\n" + noProperty + "\n");

		assertThat(result.findings()).extracting(CatalogFileParser.CatalogFinding::column)
			.containsExactly("env_property");
	}

	@Test
	void aSecretRowWithADefaultFails() {
		String secretWithDefault = row("s1", "ENVIRONMENT", "STRING", "", "", "", "x", "GLOBAL", false, "RW-COE", "DEV",
				"SOMEWHERE", true, "SECRET", "", "A description.");

		CatalogFileParser.Result result = CatalogFileParser.parse(
				CatalogFileParser.HEADER + "\n" + secretWithDefault + "\n");

		assertThat(result.findings()).extracting(CatalogFileParser.CatalogFinding::column)
			.containsExactlyInAnyOrder("default_value", "secret");
	}
}
