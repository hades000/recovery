package th.co.scb.ace.demo.recovery.architecture.migration.rule;

import static org.assertj.core.api.Assertions.assertThat;

import org.junit.jupiter.api.Test;

import th.co.scb.ace.demo.recovery.architecture.migration.MigrationLexer;
import th.co.scb.ace.demo.recovery.architecture.migration.MigrationStatement;
import th.co.scb.ace.demo.recovery.architecture.migration.ParsedMigrationFile;

/**
 * SPEC-RWB-E1-044-016 (CODE-001): the seam method receives the statement that owns the qualifier,
 * found by its offset range, so a qualifier on a later line of a multi-line statement is not null.
 */
class LiteralSchemaRuleTest {

	@Test
	void aQualifierOnALaterLineOfAMultiLineStatementFindsItsStatement() {
		ParsedMigrationFile file = MigrationLexer.parse("V0001__rwb_e1_044_ok.sql", """
				-- Story: RWB-E1-044
				CREATE TABLE ${recoverySchema}.t (
				  id int REFERENCES public.t1(id)
				);
				""");
		int offset = file.identifierText().indexOf("public");

		assertThat(file.lineOf(offset)).isEqualTo(3);
		MigrationStatement statement = LiteralSchemaRule.statementAt(file, offset);
		assertThat(statement).isNotNull();
		assertThat(statement.startLine()).isEqualTo(2);
		assertThat(LiteralSchemaRule.isAllowedQualifier(statement, "public")).isFalse();
		assertThat(LiteralSchemaRule.isAllowedQualifier(statement, "pg_catalog")).isTrue();
	}

}
