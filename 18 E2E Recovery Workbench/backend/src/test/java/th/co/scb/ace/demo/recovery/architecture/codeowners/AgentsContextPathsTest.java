package th.co.scb.ace.demo.recovery.architecture.codeowners;

import static org.assertj.core.api.Assertions.assertThat;

import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Path;
import java.util.ArrayList;
import java.util.List;
import java.util.regex.Matcher;
import java.util.regex.Pattern;

import org.junit.jupiter.api.Tag;
import org.junit.jupiter.api.Test;

/** RWB-TE-002 UT-22 (SPEC-016, A-05): every back-quoted path in the AGENTS.md §5 table exists from the repository root. */
@Tag("codeowners")
class AgentsContextPathsTest {

	private static final Pattern QUOTED = Pattern.compile("`([^`]+)`");

	@Test
	void everySectionFivePathExists() throws IOException {
		Path root = CodeOwnersValidator.repositoryRoot();
		List<String> lines = Files.readAllLines(root.resolve("AGENTS.md"));
		int start = lines.indexOf("## 5. What the agent reads besides the story");
		assertThat(start).as("AGENTS.md section 5 heading").isNotNegative();

		List<String> paths = new ArrayList<>();
		for (String line : lines.subList(start + 1, lines.size())) {
			if (line.startsWith("## ")) {
				break;
			}
			if (line.startsWith("|")) {
				Matcher quoted = QUOTED.matcher(line.split("\\|")[1]);
				while (quoted.find()) {
					paths.add(quoted.group(1));
				}
			}
		}

		assertThat(paths).hasSize(6);
		assertThat(paths).allSatisfy(path -> assertThat(root.resolve(path)).as(path).isRegularFile());
	}
}
