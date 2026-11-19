package th.co.scb.ace.demo.recovery.architecture.parameters;

import static org.assertj.core.api.Assertions.assertThat;

import java.util.List;

import org.junit.jupiter.api.Test;

/**
 * TC-E1-042-43 (SPEC-RWB-E1-042-004, finding 131): the tokenizer blanks comments, keeps the
 * content of string, text-block and char literals, and preserves offsets and line numbers.
 */
class JavaLiteralTokenizerTest {

	private static String lineOf(JavaLiteralTokenizer.Result result, int oneBasedLine) {
		return result.masked().lines().toList().get(oneBasedLine - 1);
	}

	@Test
	void commentsStringsTextBlocksAndChars() {
		String source = String.join("\n",
				"int a = 1; // literal 42 in a line comment",
				"/* block 43",
				"   still a comment 44 */",
				"String s = \"value 45\";",
				"String t = \"\"\"",
				"    text block 46",
				"    \"\"\";",
				"char c = '4';",
				"int b = 2;",
				"");

		JavaLiteralTokenizer.Result result = JavaLiteralTokenizer.tokenize(source);

		assertThat(result.literals()).extracting(JavaLiteralTokenizer.Token::text)
			.containsExactly("value 45", "\n    text block 46\n    ", "4");
		assertThat(result.literals()).extracting(JavaLiteralTokenizer.Token::kind)
			.containsExactly(JavaLiteralTokenizer.Kind.STRING, JavaLiteralTokenizer.Kind.TEXT_BLOCK,
					JavaLiteralTokenizer.Kind.CHAR);
		assertThat(result.masked()).doesNotContain("42", "43", "44", "45", "46");
		// Line numbering survives the blanking: line 1 is the `int a` line and line 9 the `int b` line.
		assertThat(lineOf(result, 1)).contains("int a = 1;");
		assertThat(lineOf(result, 2)).isBlank();
		assertThat(lineOf(result, 3)).isBlank();
		assertThat(lineOf(result, 9)).contains("int b = 2;");
	}

	@Test
	void aSlashSlashInsideAStringIsNotAComment() {
		JavaLiteralTokenizer.Result result = JavaLiteralTokenizer.tokenize("String u = \"http://example\";");

		assertThat(result.literals()).extracting(JavaLiteralTokenizer.Token::text).containsExactly("http://example");
		assertThat(result.masked()).doesNotContain("example");
	}

	@Test
	void aQuoteInsideACommentIsNotAString() {
		JavaLiteralTokenizer.Result result = JavaLiteralTokenizer.tokenize("int a = 1; // a \" quote 77");

		assertThat(result.literals()).isEmpty();
		assertThat(result.masked()).doesNotContain("77", "quote");
		assertThat(result.masked()).contains("int a = 1;");
	}

	@Test
	void tokenLinesAreOneBasedAndFollowTheOpeningDelimiter() {
		String source = String.join("\n",
				"// comment",
				"String a = \"one\";",
				"String b = \"\"\"",
				"    two",
				"    \"\"\";",
				"");

		JavaLiteralTokenizer.Result result = JavaLiteralTokenizer.tokenize(source);

		assertThat(result.literals()).extracting(JavaLiteralTokenizer.Token::line).containsExactly(2, 3);
		List<JavaLiteralTokenizer.Token> literals = result.literals();
		assertThat(literals.get(0).text()).isEqualTo("one");
		assertThat(literals.get(1).text()).isEqualTo("\n    two\n    ");
	}

	@Test
	void anUnterminatedBlockCommentIsBlankedToTheEnd() {
		JavaLiteralTokenizer.Result result = JavaLiteralTokenizer.tokenize("int a = 1; /* never closed 88");

		assertThat(result.masked()).doesNotContain("88");
		assertThat(result.literals()).isEmpty();
	}

	@Test
	void anEscapedQuoteDoesNotEndTheString() {
		JavaLiteralTokenizer.Result result = JavaLiteralTokenizer.tokenize("String s = \"a \\\" b\";");

		assertThat(result.literals()).extracting(JavaLiteralTokenizer.Token::text).containsExactly("a \" b");
	}
}
