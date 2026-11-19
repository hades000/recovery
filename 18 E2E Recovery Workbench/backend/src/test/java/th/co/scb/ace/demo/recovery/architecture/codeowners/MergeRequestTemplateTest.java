package th.co.scb.ace.demo.recovery.architecture.codeowners;

import static org.assertj.core.api.Assertions.assertThat;

import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Path;
import java.util.List;

import org.junit.jupiter.api.Tag;
import org.junit.jupiter.api.Test;

/** RWB-TE-002 UT-21 (SPEC-015, A-10): the default MR template carries the eight AGENTS.md §8 headings in order. */
@Tag("codeowners")
class MergeRequestTemplateTest {

	@Test
	void templateHasTheEightHeadingsInOrder() throws IOException {
		Path template = CodeOwnersValidator.repositoryRoot().resolve(".gitlab/merge_request_templates/Default.md");

		assertThat(template).isRegularFile();
		List<String> headings = Files.readAllLines(template).stream()
			.map(String::strip)
			.filter(line -> line.startsWith("## "))
			.toList();
		assertThat(headings).containsExactly(
				"## Story key",
				"## Plan file",
				"## Acceptance criteria covered",
				"## Coding tool used",
				"## AI first-pass review summary",
				"## Reviewer",
				"## Test results",
				"## AISDLC trailers");
	}
}
