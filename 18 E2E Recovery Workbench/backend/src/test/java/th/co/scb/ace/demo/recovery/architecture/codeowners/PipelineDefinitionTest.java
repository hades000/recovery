package th.co.scb.ace.demo.recovery.architecture.codeowners;

import static org.assertj.core.api.Assertions.assertThat;

import java.io.IOException;
import java.nio.file.Files;
import java.util.List;
import java.util.Map;

import org.junit.jupiter.api.Tag;
import org.junit.jupiter.api.Test;
import org.yaml.snakeyaml.LoaderOptions;
import org.yaml.snakeyaml.Yaml;
import org.yaml.snakeyaml.constructor.SafeConstructor;

/**
 * RWB-TE-002 UT-24 (SPEC-013, flow 2): the {@code codeowners-validation} job is defined as specified.
 * Proves the definition only, not a pipeline run (HV-07).
 */
@Tag("codeowners")
class PipelineDefinitionTest {

	@Test
	@SuppressWarnings("unchecked")
	void validationJobIsDefinedAsSpecified() throws IOException {
		String ci = Files.readString(CodeOwnersValidator.repositoryRoot().resolve(".gitlab-ci.yml"));
		Map<String, Object> pipeline = new Yaml(new SafeConstructor(new LoaderOptions())).load(ci);

		assertThat(pipeline).containsKey("codeowners-validation");
		Map<String, Object> job = (Map<String, Object>) pipeline.get("codeowners-validation");
		assertThat(job).containsEntry("stage", "verify");
		assertThat(job).doesNotContainKey("rules");
		assertThat((List<String>) job.get("script"))
			.containsExactly("cd backend && ./gradlew --no-daemon codeOwnersTest codeOwnersCoverageVerification");
		Map<String, Object> artifacts = (Map<String, Object>) job.get("artifacts");
		Map<String, Object> reports = (Map<String, Object>) artifacts.get("reports");
		assertThat(reports).containsEntry("junit", "backend/build/test-results/codeOwnersTest/*.xml");
		// Security review F8: the governance job must not share (or poison) the build jobs' Gradle cache.
		Map<String, Object> cache = (Map<String, Object>) job.get("cache");
		assertThat(cache.get("key")).isNotNull().isNotEqualTo("gradle");
	}

	@Test
	void codeOwnersTestIsNeverUpToDate() throws IOException {
		// Ponytail review Nice 3: UT-26 and V9 read the whole tree, so a deleted file must still re-run the checks.
		String build = Files.readString(CodeOwnersValidator.repositoryRoot().resolve("backend/build.gradle.kts"));
		String task = build.substring(build.indexOf("val codeOwnersTest by"));

		assertThat(task.substring(0, task.indexOf("\n}"))).contains("outputs.upToDateWhen { false }");
	}
}
