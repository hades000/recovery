package th.co.scb.ace.demo.recovery.architecture;

import static org.assertj.core.api.Assertions.assertThat;
import static org.assertj.core.api.Assertions.assertThatThrownBy;

import java.io.IOException;
import java.io.UncheckedIOException;
import java.nio.file.Files;
import java.nio.file.Path;
import java.util.ArrayList;
import java.util.LinkedHashMap;
import java.util.List;
import java.util.Map;
import java.util.stream.Stream;

import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.io.TempDir;
import org.junit.jupiter.params.ParameterizedTest;
import org.junit.jupiter.params.provider.Arguments;
import org.junit.jupiter.params.provider.MethodSource;

import th.co.scb.ace.demo.recovery.architecture.migration.MigrationFinding;
import th.co.scb.ace.demo.recovery.architecture.migration.MigrationLint;
import th.co.scb.ace.demo.recovery.architecture.migration.MigrationLexer;
import th.co.scb.ace.demo.recovery.architecture.migration.MigrationStatement;
import th.co.scb.ace.demo.recovery.architecture.migration.ParsedMigrationFile;

/**
 * SPEC-RWB-E1-044-004, -010 (T-044-01 to T-044-07, -20 to -22): the migration lint as a unit test.
 *
 * <p>The production folder must stay green on its README only, and every fixture folder asserts its
 * <em>complete</em> finding list (rule, file, line and, where two findings share a line, the key), so
 * a missing finding and an extra finding both fail. Fixture paths follow {@code data-model.md} §3;
 * {@code data-model.md} §4 holds the Flyway fixtures.
 */
class RecoveryMigrationLintTest {

	static final Path MIGRATIONS = Path.of("src/main/resources/db/modulemigration/recovery");

	static final Path FIXTURES = Path.of("src/test/resources/migration-lint");

	private static final String OK = "V0001__rwb_e1_044_ok.sql";

	/** Rule order is {@code MigrationRules.all()}; a fixture folder asserts its whole list. */
	private static final Map<String, List<String>> EXPECTED = expected();

	@Test
	void migrationsFollowTheRecoveryRules() {
		assertThat(MigrationLint.lint(MIGRATIONS)).isEmpty();
	}

	@ParameterizedTest(name = "{0}")
	@MethodSource("fixtureFolders")
	void fixtureFolderGivesExactlyTheExpectedFindings(String folder) {
		List<String> actual = render(MigrationLint.lint(FIXTURES.resolve(folder)));
		List<String> expected = EXPECTED.get(folder);

		assertThat(actual).as("complete finding list of %s", folder).hasSameSizeAs(expected);
		for (int i = 0; i < expected.size(); i++) {
			if (expected.get(i).endsWith("/*")) {
				assertThat(actual.get(i)).as("finding %d of %s", i, folder)
					.startsWith(expected.get(i).substring(0, expected.get(i).length() - 1));
			}
			else {
				assertThat(actual.get(i)).as("finding %d of %s", i, folder).isEqualTo(expected.get(i));
			}
		}
	}

	static Stream<Arguments> fixtureFolders() {
		return EXPECTED.keySet().stream().map(Arguments::of);
	}

	@Test
	void findingsUseTheMessageP3LineFormat() {
		List<MigrationFinding> findings = MigrationLint.lint(FIXTURES.resolve("t06-format-fail"));

		assertThat(findings).hasSize(2);
		assertThat(findings.get(0).format())
			.isEqualTo("MSG-P3-016 schema=recovery object=V0001__rwb_044_bad.sql:0 rule=L-NAME "
					+ "name must be V<seq>__<story>_<name>.sql");
		assertThat(findings.get(1).format())
			.isEqualTo("MSG-P3-016 schema=recovery object=V0002__rwb_e1_044_ok.sql:2 rule=L-LITERAL-SCHEMA "
					+ "literal schema recovery");
		assertThat(findings).extracting(MigrationFinding::toString).containsExactlyElementsOf(
				findings.stream().map(MigrationFinding::format).toList());
	}

	/** T-044-22 statement-view case S1: a leading comment never supplies the kind or the line. */
	@Test
	void leadingCommentsDoNotSupplyTheStatementKind() throws IOException {
		ParsedMigrationFile file = MigrationLexer.parse(FIXTURES.resolve("t22-s1").resolve(OK));

		assertThat(file.statements()).hasSize(2);
		assertThat(file.statements()).extracting(MigrationStatement::startLine).containsExactly(3, 3);
		assertThat(file.statements()).extracting(MigrationStatement::kind).containsExactly("CREATE TABLE", "INSERT");
		assertThat(MigrationLint.lint(FIXTURES.resolve("t22-s1"))).isEmpty();
	}

	@Test
	void anEmptyFolderGivesNoFinding(@TempDir Path folder) {
		assertThat(MigrationLint.lint(folder)).isEmpty();
	}

	@Test
	void aMissingFolderFailsClosed() {
		Path missing = FIXTURES.resolve("does-not-exist");

		assertThatThrownBy(() -> MigrationLint.lint(missing)).isInstanceOf(UncheckedIOException.class)
			.hasMessageContaining(missing.toString());
	}

	@Test
	void anUnreadableSqlEntryFailsClosed(@TempDir Path folder) throws IOException {
		Path unreadable = Files.createDirectory(folder.resolve("V0002__rwb_e1_044_unreadable.sql"));

		assertThatThrownBy(() -> MigrationLint.lint(folder)).isInstanceOf(UncheckedIOException.class)
			.hasMessageContaining(unreadable.getFileName().toString());
	}

	private static List<String> render(List<MigrationFinding> findings) {
		List<String> rendered = new ArrayList<>();
		for (MigrationFinding finding : findings) {
			rendered.add(finding.ruleId() + "/" + finding.file() + "/" + finding.line() + "/"
					+ (finding.key() == null ? "-" : finding.key()));
		}
		return rendered;
	}

	private static Map<String, List<String>> expected() {
		Map<String, List<String>> expected = new LinkedHashMap<>();
		expected.put("t01-pass", List.of());
		expected.put("t01-readme-pass", List.of());
		expected.put("t01-name-fail", List.of("L-NAME/V0002__rwb_044_bad.sql/0/V0002__rwb_044_bad.sql"));
		expected.put("t01-nonsql-fail", List.of("L-NAME/notes.txt/0/notes.txt"));
		expected.put("t01-undo-fail", List.of("L-UNDO/U0001__rwb_e1_044_undo.sql/0/U0001__rwb_e1_044_undo.sql"));
		expected.put("t01-repeatable-fail", List.of("L-REPEATABLE/R__views.sql/0/R__views.sql"));
		expected.put("t01-seqgap-fail", List.of("L-SEQ-GAP/V0002/0/V0002"));
		expected.put("t01-seqzero-fail", List.of("L-SEQ-GAP/V0000/0/V0000"));
		expected.put("t01-seqdup-fail", List.of("L-SEQ-DUP/V0001__rwb_e1_045_dup.sql/0/0001"));
		expected.put("t03-header-fail", List.of("L-HEADER/" + OK + "/1/-"));
		expected.put("t03-header-multi-fail", List.of("L-HEADER-MULTI/" + OK + "/3/-"));
		expected.put("t03-header-multi-indented-fail", List.of("L-HEADER-MULTI/" + OK + "/3/-"));
		expected.put("t03-keydup-fail", List.of("L-KEY-DUP/V0002__rwb_e1_028_b.sql/0/RWB-E1-028"));
		expected.put("t03-fix-line2-fail", List.of("L-FIX-LINE2/V0002__rwb_e1_044_fix.sql/2/-"));
		expected.put("t03-fix-nobase-fail", List.of("L-FIX-NO-BASE/V0002__rwb_e1_028_fix.sql/0/RWB-E1-028"));
		expected.put("t03-fix-pass", List.of());
		expected.put("t02-positions-fail", positions());
		expected.put("t02-unknown-positions-fail", unknownPositions());
		expected.put("t02-types-fail", List.of("L-LITERAL-SCHEMA/" + OK + "/2/public", "L-LITERAL-SCHEMA/" + OK + "/3/public",
				"L-LITERAL-SCHEMA/" + OK + "/4/public"));
		expected.put("t02-column-type-fail", List.of(literal(2, "rwb_case"), literal(5, "rwb_case"), literal(7, "rwb_case"),
				literal(8, "rwb_case"), literal(9, "rwb_case"), literal(10, "rwb_case"), literal(11, "rwb_case")));
		expected.put("t02-column-type-pass", List.of());
		expected.put("t02-schema-bare-fail", List.of("L-LITERAL-SCHEMA/" + OK + "/2/public"));
		expected.put("t02-allowed-pass", List.of());
		expected.put("t02-join-alias-pass", List.of());
		expected.put("t02-comment-column-pass", List.of());
		expected.put("t02-comment-on-kinds-fail", commentOnKinds());
		expected.put("t02-on-quoted-name-fail", List.of(literal(2, "rwb_case"), literal(3, "rwb_case")));
		expected.put("t02-create-rule-to-fail", List.of(literal(2, "rwb_case"), literal(3, "rwb_case")));
		expected.put("t02-on-dollar-name-fail", List.of(literal(2, "rwb_case"), literal(3, "rwb_case"), literal(4, "rwb_case")));
		expected.put("t02-comment-string-pass", List.of());
		expected.put("t02-dollar-body-fail", List.of("L-LITERAL-SCHEMA/" + OK + "/3/public"));
		expected.put("t02-quoted-fail", List.of("L-LITERAL-SCHEMA/" + OK + "/2/public"));
		expected.put("t02-seam-marker-fail", List.of("L-LITERAL-SCHEMA/" + OK + "/2/public"));
		expected.put("t05-fk-public-fail",
				List.of("L-LITERAL-SCHEMA/" + OK + "/2/public", "L-FK-OUTSIDE/" + OK + "/2/public"));
		expected.put("t05-fk-pgcatalog-fail", List.of("L-FK-OUTSIDE/" + OK + "/2/pg_catalog"));
		expected.put("t05-fk-pass", List.of());
		expected.put("t05-fk-split-fail",
				List.of("L-LITERAL-SCHEMA/" + OK + "/2/public", "L-FK-OUTSIDE/" + OK + "/2/public"));
		expected.put("t06-format-fail", List.of("L-NAME/V0001__rwb_044_bad.sql/0/V0001__rwb_044_bad.sql",
				"L-LITERAL-SCHEMA/V0002__rwb_e1_044_ok.sql/2/recovery"));
		expected.put("t20-searchpath-fail", searchPaths());
		expected.put("t20-grant-fail", List.of("L-GRANT/" + OK + "/2/-", "L-GRANT/" + OK + "/3/-",
				"L-GRANT/" + OK + "/4/-"));
		expected.put("t20-grant-tab-fail", List.of("L-GRANT/" + OK + "/4/-", "L-GRANT/" + OK + "/5/-",
				"L-GRANT/" + OK + "/10/-", "L-GRANT/" + OK + "/11/-"));
		expected.put("t20-grant-word-pass", List.of());
		expected.put("t20-grant-pass", List.of());
		expected.put("t20-grant-quoted-pass", List.of());
		expected.put("t21-literals-pass", List.of());
		expected.put("t21-literal-negatives-fail", List.of("L-LITERAL-SCHEMA/" + OK + "/4/public",
				"L-LITERAL-SCHEMA/" + OK + "/5/public", "L-LITERAL-SCHEMA/" + OK + "/6/public",
				"L-FK-OUTSIDE/" + OK + "/6/public"));
		expected.put("t21-split-qualifier-fail", List.of("L-LITERAL-SCHEMA/" + OK + "/2/public",
				"L-LITERAL-SCHEMA/" + OK + "/4/public"));
		expected.put("t22-n1", literal(3));
		expected.put("t22-n2", literal(2));
		expected.put("t22-n3", literal(3));
		expected.put("t22-n4", literal(2));
		expected.put("t22-n5", literal(2));
		expected.put("t22-n6", literal(2));
		expected.put("t22-n7", literal(3));
		expected.put("t22-n8", literal(3));
		expected.put("t22-n9", literal(4));
		expected.put("t22-n10", literal(2));
		expected.put("t22-n11", List.of("L-LITERAL-SCHEMA/" + OK + "/3/public", "L-LEX/" + OK + "/2/*"));
		expected.put("t22-n12", List.of("L-LITERAL-SCHEMA/" + OK + "/3/public", "L-LEX/" + OK + "/2/*"));
		expected.put("t22-n13", List.of("L-LITERAL-SCHEMA/" + OK + "/3/public", "L-LEX/" + OK + "/2/*"));
		expected.put("t22-n14", List.of("L-SEARCH-PATH/" + OK + "/2/-"));
		expected.put("t22-n15",
				List.of("L-LITERAL-SCHEMA/" + OK + "/2/public", "L-FK-OUTSIDE/" + OK + "/2/public"));
		expected.put("t22-p1", List.of());
		expected.put("t22-p2", List.of());
		expected.put("t22-p3", List.of());
		expected.put("t22-s1", List.of());
		return expected;
	}

	private static List<String> literal(int line) {
		return List.of(literal(line, "public"));
	}

	private static String literal(int line, String schema) {
		return "L-LITERAL-SCHEMA/" + OK + "/" + line + "/" + schema;
	}

	private static List<String> positions() {
		List<String> expected = new ArrayList<>();
		for (int line = 2; line <= 19; line++) {
			expected.add("L-LITERAL-SCHEMA/" + OK + "/" + line + "/public");
		}
		expected.add("L-FK-OUTSIDE/" + OK + "/12/public");
		return expected;
	}

	/**
	 * CONF-E044-01: every item-1 position and item-2 form with a qualifier that item 4 does not know,
	 * so only the position patterns can report it.
	 */
	private static List<String> unknownPositions() {
		List<String> expected = new ArrayList<>();
		for (int line = 2; line <= 28; line++) {
			expected.add("L-LITERAL-SCHEMA/" + OK + "/" + line + "/rwb_case");
		}
		expected.add("L-FK-OUTSIDE/" + OK + "/13/rwb_case");
		expected.add("L-GRANT/" + OK + "/26/-");
		return expected;
	}

	/**
	 * CONF2-E044-01: {@code COMMENT ON <kind>} for kinds that share no other position keyword, each with
	 * a qualifier that item 4 does not know.
	 */
	private static List<String> commentOnKinds() {
		List<String> expected = new ArrayList<>();
		for (int line = 2; line <= 15; line++) {
			expected.add(literal(line, "rwb_case"));
		}
		return expected;
	}

	private static List<String> searchPaths() {
		List<String> expected = new ArrayList<>();
		for (int line = 2; line <= 9; line++) {
			expected.add("L-SEARCH-PATH/" + OK + "/" + line + "/-");
		}
		return expected;
	}

}
