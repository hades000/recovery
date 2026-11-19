package th.co.scb.ace.demo.recovery.architecture.parameters;

import static org.assertj.core.api.Assertions.assertThat;

import java.nio.file.Path;
import java.util.List;
import java.util.Map;
import java.util.stream.Collectors;

import org.junit.jupiter.api.Test;

import th.co.scb.ace.demo.recovery.casewf.config.api.ParameterKey;
import th.co.scb.ace.demo.recovery.casewf.config.api.ParameterKeys;

/**
 * TC-E1-042-42 and TC-E1-042-26 (SPEC-RWB-E1-042-005; BR1, CON5): the generated keys equal the
 * catalog file row for row on every column, so a generator fault or a catalog edit without a
 * rebuild fails the build.
 */
class ParameterKeysGenerationTest {

	static final Path CATALOG = Path.of("src/main/resources/config/parameter-catalog.csv");

	@Test
	void generatedKeysMatchTheCatalogFile() {
		CatalogFileParser.Result catalog = CatalogFileParser.parse(CATALOG);
		List<ParameterKey<?>> generated = ParameterKeys.all();

		assertThat(generated).hasSameSizeAs(catalog.rows());
		assertThat(generated.stream().map(ParameterKey::name).toList())
			.containsExactlyElementsOf(catalog.rows().stream().map(CatalogRow::key).toList());
		Map<String, ParameterKey<?>> byName = generated.stream()
			.collect(Collectors.toMap(ParameterKey::name, key -> key));

		for (CatalogRow row : catalog.rows()) {
			ParameterKey<?> key = byName.get(row.key());
			assertThat(key.kind()).as(row.key() + " kind").isEqualTo(row.kind());
			assertThat(typeName(key)).as(row.key() + " type").isEqualTo(row.valueType());
			assertThat(key.unit()).as(row.key() + " unit").isEqualTo(row.unit());
			assertThat(key.min()).as(row.key() + " min").isEqualTo(row.minValue());
			assertThat(key.max()).as(row.key() + " max").isEqualTo(row.maxValue());
			assertThat(key.defaultValue()).as(row.key() + " default").isEqualTo(row.defaultValue().isEmpty()
					? null : row.defaultValue());
			assertThat(key.scope()).as(row.key() + " scope").isEqualTo(row.scope());
			assertThat(key.required()).as(row.key() + " required").isEqualTo(row.required());
			assertThat(key.ownerRole()).as(row.key() + " owner").isEqualTo(row.ownerRole());
			assertThat(key.environments()).as(row.key() + " environments").isEqualTo(row.environments());
			assertThat(key.usedBy()).as(row.key() + " usedBy").isEqualTo(row.usedBy());
			assertThat(key.secret()).as(row.key() + " secret").isEqualTo(row.secret());
			assertThat(key.valueSource()).as(row.key() + " valueSource").isEqualTo(row.valueSource());
			assertThat(key.envProperty()).as(row.key() + " envProperty").isEqualTo(row.envProperty().isEmpty()
					? null : row.envProperty());
			assertThat(key.description()).as(row.key() + " description").isEqualTo(row.description());
		}
	}

	/** SEC-042-02: the emitted class is valid Java with escaped strings and literal booleans only. */
	@Test
	void theGeneratedSourceEscapesStringsAndEmitsLiteralBooleans() throws java.io.IOException {
		java.nio.file.Path generated = Path.of(
				"build/generated/sources/parameterKeys/th/co/scb/ace/demo/recovery/casewf/config/api/ParameterKeys.java");
		String source = java.nio.file.Files.readString(generated, java.nio.charset.StandardCharsets.UTF_8);

		assertThat(source).doesNotContain("\u0000").doesNotContain("\u0007");
		for (String line : source.lines().toList()) {
			// Every emitted string literal closes on its own line: no raw newline inside a literal.
			long quotes = line.chars().filter(character -> character == '"').count();
			assertThat(quotes % 2).as("unbalanced quotes in: " + line).isZero();
		}
		assertThat(source).contains(", true,").contains(", false,");
		assertThat(source).doesNotContain("System.out").doesNotContain("static {");
	}

	@Test
	void typedConstantsExist() {
		assertThat(ParameterKeys.CASE_ENTRY_DPD.type()).isEqualTo(Integer.class);
		assertThat(ParameterKeys.CASE_ENTRY_DPD.name()).isEqualTo("case.entry.dpd");
		assertThat(ParameterKeys.SERVICELEVEL_REQUIRED_STATUSES.type()).isEqualTo(List.class);
		assertThat(ParameterKeys.CASELIST_ALLOCATION_WAIT_UNTIL.type().getName()).isEqualTo("java.time.LocalTime");
		assertThat(ParameterKeys.TEMPORAL_NAMESPACE.defaultValue()).isEqualTo("rwb-recovery");
		assertThat(ParameterKeys.ACE_DB_PASSWORD.secret()).isTrue();
		assertThat(ParameterKeys.TEMPORAL_TARGET.defaultValue()).isNull();
		assertThat(ParameterKeys.ENTRY_DPD.scope()).isEqualTo("PRODUCT");
	}

	@Test
	void byNameFindsTheConstantAndRefusesTheWrongType() {
		assertThat(ParameterKeys.byName("case.entry.dpd", Integer.class)).contains(ParameterKeys.CASE_ENTRY_DPD);
		assertThat(ParameterKeys.byName("case.entry.dpd", String.class)).isEmpty();
		assertThat(ParameterKeys.byName("not.a.key", Integer.class)).isEmpty();
	}

	private static String typeName(ParameterKey<?> key) {
		Class<?> type = key.type();
		if (type == Integer.class) {
			return "INTEGER";
		}
		if (type == java.math.BigDecimal.class) {
			return "DECIMAL";
		}
		if (type == Boolean.class) {
			return "BOOLEAN";
		}
		if (type == java.time.LocalDate.class) {
			return "DATE";
		}
		if (type == java.time.LocalTime.class) {
			return "TIME";
		}
		if (type == java.time.Duration.class) {
			return "DURATION";
		}
		return type == List.class ? "CODE_LIST" : "STRING";
	}
}
