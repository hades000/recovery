package th.co.scb.ace.demo.recovery.architecture.migration;

import static org.assertj.core.api.Assertions.assertThat;
import static org.assertj.core.api.Assertions.assertThatThrownBy;
import static org.junit.jupiter.api.Assertions.assertTimeoutPreemptively;

import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Path;
import java.time.Duration;
import java.util.Arrays;

import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.io.TempDir;

/**
 * SPEC-RWB-E1-044-007 (T-044-22): the one quote-aware tokenizer pass and the three views.
 *
 * <p>Comments and strings are never removed by separate passes: a {@code /*} inside a literal or a
 * quote inside a comment must not hide real code. Every case here is one of the T-044-22 shapes or
 * a token kind from the SPEC-007 table.
 */
class MigrationLexerTest {

	private static final String HEADER = "-- Story: RWB-E1-044\n";

	@Test
	void lineCommentBlanksToTheEndOfTheLineOnly() {
		ParsedMigrationFile file = parse("SELECT 1; -- public.x\nSELECT 2;\n");

		assertThat(file.identifierText()).doesNotContain("public.x").contains("SELECT 2");
		assertThat(file.codeText()).doesNotContain("public.x").contains("SELECT 2");
		assertThat(file.statements()).hasSize(2);
	}

	@Test
	void blockCommentNestsLikePostgres() {
		ParsedMigrationFile file = parse("/* outer /* inner */ public.x */ SELECT 1;\n");

		assertThat(file.identifierText()).doesNotContain("public").contains("SELECT 1");
		assertThat(file.unterminated()).isEmpty();
	}

	@Test
	void standardStringHandlesADoubledQuoteAndHidesItsContent() {
		ParsedMigrationFile file = parse("SELECT 'it''s public.x'; SELECT 1;\n");

		assertThat(file.identifierText()).doesNotContain("public").doesNotContain("it");
		assertThat(file.codeText()).contains("'it''s public.x'");
		assertThat(file.statements()).as("a ; inside a string never cuts a statement").hasSize(2);
	}

	@Test
	void escapeStringHandlesBackslashEscapedQuoteAndBackslash() {
		ParsedMigrationFile file = parse("SELECT E'\\'--', E'a\\\\'; SELECT 1;\n");

		assertThat(file.identifierText()).doesNotContain("--");
		assertThat(file.codeText()).contains("E'\\'--'");
		assertThat(file.statements()).hasSize(2);
	}

	@Test
	void quotedIdentifierKeepsItsTextAndADoubledQuote() {
		ParsedMigrationFile file = parse("CREATE TABLE recovery.\"a--b\" (id int);\n");

		assertThat(file.identifierText()).contains("\"a--b\"");
		assertThat(file.codeText()).contains("\"a--b\"");
		assertThat(file.identifierText()).as("the -- inside the identifier starts no comment").contains("(id int)");
		assertThat(file.statements()).hasSize(1);
	}

	@Test
	void aPlaceholderIsIdentifierTextAndNeverADollarQuote() {
		ParsedMigrationFile file = parse("CREATE TABLE ${recoverySchema}.t (id int);\n");

		assertThat(file.identifierText()).contains("${recoverySchema}");
		assertThat(file.unterminated()).isEmpty();
		assertThat(file.statements()).hasSize(1);
	}

	@Test
	void aDollarParameterIsNotAQuote() {
		ParsedMigrationFile file = parse("SELECT $1, $2;\n");

		assertThat(file.unterminated()).isEmpty();
		assertThat(file.statements()).hasSize(1);
	}

	@Test
	void aDollarBodyIsKeptAsCodeAndItsOwnSemicolonsNeverCut() {
		ParsedMigrationFile file = parse("CREATE FUNCTION f() RETURNS int AS $$ SELECT 1 -- $$\n; SELECT 2;\n");

		assertThat(file.unterminated()).isEmpty();
		assertThat(file.identifierText()).contains("SELECT 1");
		assertThat(file.statements()).as("the body end, not the ; inside the body, is code").hasSize(2);
	}

	@Test
	void aTaggedDollarBodyEndsAtItsOwnTagAndTheBodyEndWinsOverAnOpenComment() {
		ParsedMigrationFile file = parse("CREATE FUNCTION g() RETURNS int AS $fn$ SELECT 1 /* $fn$\n; SELECT 3;\n");

		assertThat(file.unterminated()).isEmpty();
		assertThat(file.identifierText()).contains("SELECT 3");
		assertThat(file.statements()).hasSize(2);
	}

	@Test
	void anOpenerInsideAnotherTokenDoesNotOpenAToken() {
		ParsedMigrationFile file = parse(HEADER
				+ "INSERT INTO ${recoverySchema}.t (v) VALUES ('/*'); -- a quote ' and a block opener\n"
				+ "CREATE TABLE ${recoverySchema}.x (id int);\n");

		assertThat(file.unterminated()).isEmpty();
		assertThat(file.statements()).hasSize(2);
		assertThat(file.identifierText()).doesNotContain("a quote");
	}

	@Test
	void eachUnterminatedOpenerGivesOneProblemOnTheOpenerLine() {
		assertThat(parse("SELECT 1;\nSELECT 'abc\n").unterminated()).singleElement()
			.satisfies(problem -> {
				assertThat(problem.kind()).isEqualTo("string");
				assertThat(problem.line()).isEqualTo(2);
			});
		assertThat(parse("SELECT 1;\nSELECT E'abc\n").unterminated()).singleElement()
			.satisfies(problem -> {
				assertThat(problem.kind()).isEqualTo("escape string");
				assertThat(problem.line()).isEqualTo(2);
			});
		assertThat(parse("SELECT 1;\nSELECT \"abc\n").unterminated()).singleElement()
			.satisfies(problem -> {
				assertThat(problem.kind()).isEqualTo("quoted identifier");
				assertThat(problem.line()).isEqualTo(2);
			});
		assertThat(parse("SELECT 1;\n/* not closed\n").unterminated()).singleElement()
			.satisfies(problem -> {
				assertThat(problem.kind()).isEqualTo("block comment");
				assertThat(problem.line()).isEqualTo(2);
			});
		assertThat(parse("SELECT 1;\nDO $q$ BEGIN NULL; END;\n").unterminated()).singleElement()
			.satisfies(problem -> {
				assertThat(problem.kind()).isEqualTo("dollar-quoted body");
				assertThat(problem.line()).isEqualTo(2);
			});
	}

	@Test
	void anUnterminatedOpenerIsOneCodeCharacterAndTheRestOfTheFileIsStillRead() {
		ParsedMigrationFile file = parse("/* not closed\nCREATE TABLE ${recoverySchema}.x (id int);\n");

		assertThat(file.identifierText()).contains("CREATE TABLE ${recoverySchema}.x");
	}

	@Test
	void statementsAreCutAtTopLevelSemicolonsAndReadLineAndKind() {
		ParsedMigrationFile file = parse(HEADER
				+ "CREATE TABLE ${recoverySchema}.t (id int);\n"
				+ "INSERT INTO ${recoverySchema}.t (id) VALUES (1);\n");

		assertThat(file.statements()).hasSize(2);
		MigrationStatement first = file.statements().get(0);
		MigrationStatement second = file.statements().get(1);
		assertThat(first.startLine()).isEqualTo(2);
		assertThat(first.firstWord()).isEqualTo("CREATE");
		assertThat(first.kind()).isEqualTo("CREATE TABLE");
		assertThat(second.startLine()).isEqualTo(3);
		assertThat(second.kind()).isEqualTo("INSERT");
		assertThat(file.identifierText().substring(first.startOffset(), first.endOffset())).startsWith("CREATE TABLE");
	}

	@Test
	void aRangeWithNoNonBlankIdentifierTextIsNotAStatement() {
		ParsedMigrationFile file = parse("SELECT 1; -- trailing\n\n/* x */\n");

		assertThat(file.statements()).hasSize(1);
	}

	/** T-044-22 statement-view case S1: a leading comment never supplies the kind or the line. */
	@Test
	void leadingCommentsDoNotSupplyTheStatementKind() {
		ParsedMigrationFile file = parse(HEADER
				+ "/* CREATE VIEW v */ -- GRANT x\n"
				+ "CREATE TABLE ${recoverySchema}.t (id int); INSERT INTO ${recoverySchema}.t (id) VALUES (1);\n");

		assertThat(file.statements()).hasSize(2);
		assertThat(file.statements()).extracting(MigrationStatement::startLine).containsExactly(3, 3);
		assertThat(file.statements()).extracting(MigrationStatement::kind).containsExactly("CREATE TABLE", "INSERT");
	}

	@Test
	void aFileAtTheSizeLimitParsesAndOneCharacterMoreFailsClosed() {
		String atLimit = "SELECT 1;\n" + " ".repeat(262_144 - 10);

		assertThat(MigrationLexer.parse("V0001__rwb_e1_044_ok.sql", atLimit).statements()).hasSize(1);
		assertThatThrownBy(() -> MigrationLexer.parse("V0001__rwb_e1_044_ok.sql", atLimit + " "))
			.isInstanceOf(IllegalArgumentException.class)
			.hasMessageContaining("262144")
			.hasMessageContaining("V0001__rwb_e1_044_ok.sql");
	}

	@Test
	void repeatedUnterminatedBlockCommentsStayLinear() {
		String text = "/*".repeat(100_000);

		assertTimeoutPreemptively(Duration.ofSeconds(5), () -> {
			ParsedMigrationFile file = MigrationLexer.parse("V0001__rwb_e1_044_ok.sql", text);

			assertThat(file.unterminated()).hasSize(100_000);
			assertThat(file.unterminated().get(99_999).line()).isEqualTo(1);
		});
	}

	@Test
	void deeplyNestedDollarBodiesFailClosedAtTheBound() {
		StringBuilder text = new StringBuilder();
		for (int level = 0; level < 40; level++) {
			text.append("$t").append(level).append("$ ");
		}
		text.append("SELECT 1");
		for (int level = 39; level >= 0; level--) {
			text.append(" $t").append(level).append("$");
		}

		assertThatThrownBy(() -> MigrationLexer.parse("V0001__rwb_e1_044_ok.sql", text.toString()))
			.isInstanceOf(IllegalArgumentException.class)
			.hasMessageContaining("nesting");
	}

	@Test
	void aSmallDollarNestingDepthIsAccepted() {
		StringBuilder text = new StringBuilder();
		for (int level = 0; level < 5; level++) {
			text.append("$t").append(level).append("$ ");
		}
		text.append("SELECT 1");
		for (int level = 4; level >= 0; level--) {
			text.append(" $t").append(level).append("$");
		}

		assertThat(MigrationLexer.parse("V0001__rwb_e1_044_ok.sql", text.toString()).unterminated()).isEmpty();
	}

	@Test
	void anOverLimitFileFailsOnItsSizeBeforeItIsRead(@TempDir Path folder) throws IOException {
		byte[] bytes = new byte[262_145];
		Arrays.fill(bytes, (byte) 0xFF);
		Path file = Files.write(folder.resolve("V0001__rwb_e1_044_ok.sql"), bytes);

		assertThatThrownBy(() -> MigrationLexer.parse(file)).isInstanceOf(IllegalArgumentException.class)
			.hasMessageContaining("larger than");
	}

	@Test
	void anUnterminatedNestedBlockCommentIsReportedOnce() {
		ParsedMigrationFile file = parse("/* /* */\n");

		assertThat(file.unterminated()).singleElement().satisfies(problem -> {
			assertThat(problem.kind()).isEqualTo("block comment");
			assertThat(problem.line()).isEqualTo(1);
		});
	}

	private static ParsedMigrationFile parse(String text) {
		return MigrationLexer.parse("V0001__rwb_e1_044_ok.sql", text);
	}

}
