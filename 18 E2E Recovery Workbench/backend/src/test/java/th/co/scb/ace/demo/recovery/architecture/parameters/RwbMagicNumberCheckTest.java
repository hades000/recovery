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
 * TC-E1-042-02 and TC-E1-042-25 (SPEC-RWB-E1-042-004; AC2, BR1, X1, GR1): a business literal fails
 * the build naming file, line and catalog key, an unlisted literal fails, and a stale baseline entry
 * fails.
 */
class RwbMagicNumberCheckTest {

	static final Path MAIN = Path.of("src/main/java");

	static final Path FIXTURES = Path.of("src/test/resources/architecture/fixtures/parameter-checks");

	static final Path BASELINE = Path.of("src/test/resources/architecture/magic-number-baseline.csv");

	static final Path CATALOG = Path.of("src/main/resources/config/parameter-catalog.csv");

	private static CatalogFileParser.Result catalog() {
		return CatalogFileParser.parse(CATALOG);
	}

	private static Path write(Path root, String relative, String body) throws IOException {
		Path file = root.resolve(relative);
		Files.createDirectories(file.getParent());
		Files.writeString(file, body, StandardCharsets.UTF_8);
		return file;
	}

	@Test
	void literalNinetyFailsNamingFileLineAndKey() {
		List<MagicNumberBaseline.Finding> findings = MagicNumberBaseline.check(
				FIXTURES.resolve("main/recovery/casewf/casecreation"), List.of(), catalog());

		assertThat(findings).hasSize(1);
		MagicNumberBaseline.Finding finding = findings.get(0);
		assertThat(finding.file()).isEqualTo("EntryRule.java");
		assertThat(finding.line()).isEqualTo(7);
		assertThat(finding.message()).contains("case.entry.dpd");
		assertThat(finding.literal()).isEqualTo("90");
	}

	@Test
	void unlistedLiteralFails(@TempDir Path root) throws IOException {
		write(root, "recovery/casewf/caselist/Unlisted.java", "class Unlisted { int a = 7; }\n");

		List<MagicNumberBaseline.Finding> findings = MagicNumberBaseline.check(root, List.of(), catalog());

		assertThat(findings).hasSize(1);
		assertThat(findings.get(0).message()).contains("is not in the baseline");
	}

	@Test
	void staleBaselineEntryFails() {
		List<MagicNumberBaseline.Entry> baseline = MagicNumberBaseline
			.read(FIXTURES.resolve("baseline/stale.csv"));

		List<MagicNumberBaseline.Finding> findings = MagicNumberBaseline.check(
				FIXTURES.resolve("main"), baseline, catalog());

		assertThat(findings).anySatisfy(finding -> assertThat(finding.message()).contains("stale"));
	}

	@Test
	void aBaselinedLiteralPasses() {
		List<MagicNumberBaseline.Entry> baseline = MagicNumberBaseline
			.read(FIXTURES.resolve("baseline/valid.csv"));

		assertThat(MagicNumberBaseline.check(FIXTURES.resolve("main"), baseline,
				catalog()))
			.isEmpty();
	}

	@Test
	void zeroOneAndMinusOnePass(@TempDir Path root) throws IOException {
		write(root, "recovery/casewf/caselist/Zero.java", "class Zero { int a = 0; int b = 1; int c = -1; }\n");

		assertThat(MagicNumberBaseline.check(root, List.of(), catalog())).isEmpty();
	}

	@Test
	void aStringEqualToANonSecretDefaultFails(@TempDir Path root) throws IOException {
		write(root, "recovery/casewf/workflow/Strings.java",
				"class Strings { String a = \"rwb-recovery\"; }\n");

		List<MagicNumberBaseline.Finding> findings = MagicNumberBaseline.check(root, List.of(), catalog());

		assertThat(findings).hasSize(1);
		assertThat(findings.get(0).message()).contains("temporal.namespace");
	}

	@Test
	void theRealMainTreePassesTheReviewedBaseline() {
		List<MagicNumberBaseline.Entry> baseline = MagicNumberBaseline.read(BASELINE);

		assertThat(MagicNumberBaseline.check(MAIN, baseline, catalog())).isEmpty();
	}
}
