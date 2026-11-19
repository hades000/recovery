package th.co.scb.ace.demo.recovery.architecture.parameters;

import static org.assertj.core.api.Assertions.assertThat;

import org.junit.jupiter.api.Test;

/**
 * TC-E1-042-43 (SPEC-RWB-E1-042-004, finding 131): numbers are normalised before matching, so a
 * reformatted literal cannot slip past the ratchet, and a number inside a comment or a string is
 * never a literal.
 */
class MagicNumberScannerTest {

	@Test
	void numericNormalisation() {
		String source = """
				int a = 10_000;
				int b = 0x1F;
				float c = 1.5f;
				long d = 2L;
				int e = -1;
				int f = 0;
				int g = 1;
				// 999 in a comment
				String s = "888";
				""";

		MagicNumberScanner.Scan scan = MagicNumberScanner.scan("Sample.java", source);

		assertThat(scan.numbers()).extracting(MagicNumberScanner.NumberLiteral::literal)
			.containsExactly("10000", "0x1f", "1.5", "2", "-1", "0", "1");
		assertThat(scan.numbers()).extracting(MagicNumberScanner.NumberLiteral::line)
			.containsExactly(1, 2, 3, 4, 5, 6, 7);
		assertThat(scan.strings()).extracting(MagicNumberScanner.StringLiteral::text).containsExactly("888");
	}

	@Test
	void aNumberInALineCommentIsNotALiteral() {
		MagicNumberScanner.Scan scan = MagicNumberScanner.scan("Sample.java", "int a = 1; // 404 here");

		assertThat(scan.numbers()).extracting(MagicNumberScanner.NumberLiteral::literal).containsExactly("1");
	}

	@Test
	void aNumberInsideATextBlockIsNotALiteral() {
		String source = String.join("\n", "String t = \"\"\"", "    500", "    \"\"\";", "int a = 1;", "");

		MagicNumberScanner.Scan scan = MagicNumberScanner.scan("Sample.java", source);

		assertThat(scan.numbers()).extracting(MagicNumberScanner.NumberLiteral::literal).containsExactly("1");
		assertThat(scan.strings()).extracting(MagicNumberScanner.StringLiteral::text).containsExactly("\n    500\n    ");
	}

	@Test
	void aSuffixAndAnExponentAreNormalised() {
		MagicNumberScanner.Scan scan = MagicNumberScanner.scan("Sample.java", "double a = 1.5D; double b = 2e3;");

		assertThat(scan.numbers()).extracting(MagicNumberScanner.NumberLiteral::literal).containsExactly("1.5", "2e3");
	}

	@Test
	void aHexLiteralKeepsItsDigitsAndIsLowerCase() {
		MagicNumberScanner.Scan scan = MagicNumberScanner.scan("Sample.java", "int mask = 0XAB_CDL;");

		assertThat(scan.numbers()).extracting(MagicNumberScanner.NumberLiteral::literal).containsExactly("0xabcd");
	}

	@Test
	void aNumberAfterAnIdentifierIsNotALiteral() {
		MagicNumberScanner.Scan scan = MagicNumberScanner.scan("Sample.java", "order2.get(3); list7.add(4);");

		assertThat(scan.numbers()).extracting(MagicNumberScanner.NumberLiteral::literal).containsExactly("3", "4");
	}
}
