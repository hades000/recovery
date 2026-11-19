package th.co.scb.ace.demo.recovery.architecture.codeowners;

import static org.assertj.core.api.Assertions.assertThat;

import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Path;
import java.util.List;

import org.junit.jupiter.api.Tag;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.io.TempDir;

/**
 * RWB-TE-002 UT-01..UT-12, UT-23 (SPEC-001, -004, -005, -008, -009, -017; AC7, BR3, BR4, BR5, BR7,
 * X6): every validation rule V1-V12 fails on its breaking fixture and passes on the live file.
 */
@Tag("codeowners")
class CodeOwnersValidationTest {

	private static final String RECOVERY_TEAM = "@scb-ace/techx-recovery-tech-leads";

	private static final String ACE_TEAM = "@scb-ace/ace-team";

	private static final String COMMON_PATTERN = "/backend/src/main/java/th/co/scb/ace/demo/common/";

	private static final String PRECEDENCE_BASIS =
			"Security review F1: GitLab reads this file before .gitlab/CODEOWNERS; it must not exist; D-RUN-25";

	private static final String REGISTER = """
			owners:
			  - handle: "@scb-ace/techx-recovery-tech-leads"
			    role: "Recovery tech leads"
			    source: "Synthetic test register v1"
			    status: ASSUMED
			    openItem: OPEN-038
			  - handle: "@scb-ace/ace-team"
			    role: "ACE team"
			    source: "Synthetic test register v1"
			    status: ASSUMED
			    openItem: OPEN-038
			  - handle: "@role-placeholder/solution-architect-with-tech-leads"
			    role: "Standards owner"
			    source: "Synthetic test register v1"
			    status: PLACEHOLDER
			    openItem: OPEN-038
			  - handle: "@role-placeholder/techx-devops-with-scb-it"
			    role: "Pipeline owner"
			    source: "Synthetic test register v1"
			    status: PLACEHOLDER
			    openItem: OPEN-038
			reservedPatterns:
			  - pattern: "/backend/src/main/java/th/co/scb/ace/demo/common/"
			    basis: "BR3; OPEN-024"
			""";

	@Test
	void malformedLineIsASyntaxError(@TempDir Path dir) throws IOException {
		Path repo = repository(dir);
		file(repo, "backend/src/main/java/th/co/scb/ace/demo/recovery/casewf/internal/AllocationService.java");
		Path codeOwners = codeOwners(dir, """
				[Recovery module]
				/backend/src/main/java/th/co/scb/ace/demo/recovery/ @scb-ace/techx-recovery-tech-leads
				[A] @x
				""");

		List<CodeOwnersValidator.Finding> findings = validate(repo, codeOwners, register(dir));

		assertThat(errors(findings)).containsExactly("line 3: syntax error");
		assertThat(CodeOwnersValidator.failed(findings)).isTrue();
	}

	@Test
	void missingFileFailsClosed(@TempDir Path dir) throws IOException {
		Path repo = repository(dir);
		Path absent = dir.resolve("absent-CODEOWNERS");

		List<CodeOwnersValidator.Finding> findings = validate(repo, absent, register(dir));

		assertThat(errors(findings)).containsExactly(".gitlab/CODEOWNERS not found");
		assertThat(CodeOwnersValidator.failed(findings)).isTrue();
	}

	@Test
	void entryOutsideASectionIsRejected(@TempDir Path dir) throws IOException {
		Path repo = repository(dir);
		file(repo, "x/keep.txt");
		Path codeOwners = codeOwners(dir, """
				/x/ @scb-ace/techx-recovery-tech-leads
				[Recovery module]
				/x/ @scb-ace/techx-recovery-tech-leads
				""");

		assertThat(errors(validate(repo, codeOwners, register(dir))))
			.containsExactly("line 1: entry outside a section");
	}

	@Test
	void patternWithoutOwnerIsRejected(@TempDir Path dir) throws IOException {
		Path repo = repository(dir);
		file(repo, "x/keep.txt");
		Path codeOwners = codeOwners(dir, """
				[Recovery module]
				/x/
				""");

		assertThat(errors(validate(repo, codeOwners, register(dir))))
			.containsExactly("line 2: pattern /x/ has no owner");
	}

	@Test
	void unsupportedPatternsAreRejected(@TempDir Path dir) throws IOException {
		Path repo = repository(dir);
		Path codeOwners = codeOwners(dir, """
				[Recovery module]
				x/ @scb-ace/techx-recovery-tech-leads
				/x/*.java @scb-ace/techx-recovery-tech-leads
				/x/**/y/ @scb-ace/techx-recovery-tech-leads
				""");

		assertThat(errors(validate(repo, codeOwners, register(dir)))).containsExactly(
				"line 2: unsupported pattern x/",
				"line 3: unsupported pattern /x/*.java",
				"line 4: unsupported pattern /x/**/y/");
	}

	@Test
	void duplicatePatternInOneSectionIsRejected(@TempDir Path dir) throws IOException {
		Path repo = repository(dir);
		file(repo, "x/keep.txt");
		Path codeOwners = codeOwners(dir, """
				[Recovery one]
				/x/ @scb-ace/techx-recovery-tech-leads
				/x/ @scb-ace/techx-recovery-tech-leads

				[Recovery two]
				/x/ @scb-ace/techx-recovery-tech-leads
				""");

		assertThat(errors(validate(repo, codeOwners, register(dir))))
			.containsExactly("line 3: duplicate pattern /x/ in section Recovery one");
	}

	@Test
	void shadowedPatternIsRejected(@TempDir Path dir) throws IOException {
		Path repo = repository(dir);
		file(repo, "a/b/keep.txt");
		Path shadowed = codeOwners(dir, """
				[Recovery module]
				/a/b/ @scb-ace/techx-recovery-tech-leads
				/a/ @scb-ace/techx-recovery-tech-leads
				""");

		assertThat(errors(validate(repo, shadowed, register(dir)))).containsExactly(
				"line 2: pattern /a/b/ is shadowed by later pattern /a/ in section Recovery module");

		Path ordered = codeOwners(dir, """
				[Recovery module]
				/a/ @scb-ace/techx-recovery-tech-leads
				/a/b/ @scb-ace/techx-recovery-tech-leads
				""");

		assertThat(errors(validate(repo, ordered, register(dir)))).isEmpty();
	}

	@Test
	void ownerNotInTheRegisterIsRejected(@TempDir Path dir) throws IOException {
		Path repo = repository(dir);
		file(repo, "backend/src/main/java/th/co/scb/ace/demo/recovery/casewf/events/CaseEvent.java");
		Path codeOwners = codeOwners(dir, """
				[Recovery module]
				/backend/src/main/java/th/co/scb/ace/demo/recovery/ @scb-ace/recovery-leads-typo
				""");

		List<CodeOwnersValidator.Finding> findings = validate(repo, codeOwners, register(dir));

		assertThat(errors(findings)).containsExactly("line 2: owner @scb-ace/recovery-leads-typo not found");
		assertThat(CodeOwnersValidator.failed(findings)).isTrue();
	}

	@Test
	void ownerThatIsNotATeamIsRejected(@TempDir Path dir) throws IOException {
		Path repo = repository(dir);
		file(repo, "x/keep.txt");
		file(repo, "y/keep.txt");
		Path codeOwners = codeOwners(dir, """
				[Recovery module]
				/x/ @someone
				/y/ someone@example.test
				""");

		assertThat(errors(validate(repo, codeOwners, register(dir)))).containsExactly(
				"line 2: owner @someone is not a team",
				"line 3: owner someone@example.test is not a team");
	}

	@Test
	void patternThatMatchesNoFileIsRejected(@TempDir Path dir) throws IOException {
		Path repo = repository(dir);
		Files.createDirectories(repo.resolve("empty"));
		Path codeOwners = codeOwners(dir, """
				[Recovery module]
				/missing/ @scb-ace/techx-recovery-tech-leads
				/empty/ @scb-ace/techx-recovery-tech-leads
				""");

		assertThat(errors(validate(repo, codeOwners, register(dir)))).containsExactly(
				"line 2: pattern /missing/ matches no file",
				"line 3: pattern /empty/ matches no file");
	}

	@Test
	void reservedPatternThatMatchesNoFileIsAWarning(@TempDir Path dir) throws IOException {
		Path repo = repository(dir);
		file(repo, "backend/src/main/java/th/co/scb/ace/demo/recovery/casewf/CaseFacade.java");
		Path codeOwners = codeOwners(dir, """
				[Common module]
				/backend/src/main/java/th/co/scb/ace/demo/common/ @scb-ace/ace-team

				[Recovery module]
				/backend/src/main/java/th/co/scb/ace/demo/recovery/ @scb-ace/techx-recovery-tech-leads
				""");

		List<CodeOwnersValidator.Finding> findings = validate(repo, codeOwners, register(dir));

		assertThat(errors(findings)).isEmpty();
		assertThat(warnings(findings)).containsExactlyInAnyOrder(
				"line 2: reserved pattern /backend/src/main/java/th/co/scb/ace/demo/common/ matches no file (BR3; OPEN-024)",
				"owner @role-placeholder/solution-architect-with-tech-leads is a placeholder for Standards owner (OPEN-038)",
				"owner @role-placeholder/techx-devops-with-scb-it is a placeholder for Pipeline owner (OPEN-038)");
		assertThat(CodeOwnersValidator.failed(findings)).isFalse();
	}

	@Test
	void malformedRegisterIsRejected(@TempDir Path dir) throws IOException {
		Path repo = repository(dir);
		file(repo, "x/keep.txt");
		Path codeOwners = codeOwners(dir, """
				[Recovery module]
				/x/ @scb-ace/ace-team
				""");

		assertThat(errors(validate(repo, codeOwners, register(dir, """
				owners:
				  - handle: "@scb-ace/ace-team"
				    source: "Synthetic test register v1"
				    status: ASSUMED
				    openItem: OPEN-038
				""")))).containsExactly("register: owners[0] field role is missing");

		assertThat(errors(validate(repo, codeOwners, register(dir, """
				owners:
				  - handle: "@scb-ace/ace-team"
				    role: "ACE team"
				    source: "Synthetic test register v1"
				    status: DRAFT
				    openItem: OPEN-038
				"""))))
			.containsExactly("register: owners[0] status DRAFT is not one of ASSUMED, PLACEHOLDER, CONFIRMED");

		assertThat(errors(validate(repo, codeOwners, register(dir, """
				owners:
				  - handle: "@scb-ace/ace-team"
				    role: "ACE team"
				    source: "Synthetic test register v1"
				    status: ASSUMED
				    openItem: OPEN-038
				  - handle: "@scb-ace/ace-team"
				    role: "ACE team"
				    source: "Synthetic test register v1"
				    status: ASSUMED
				    openItem: OPEN-038
				""")))).containsExactly("register: owners[1] handle @scb-ace/ace-team is listed twice");

		List<CodeOwnersValidator.Finding> placeholder = validate(repo, codeOwners, register(dir, """
				owners:
				  - handle: "@scb-ace/ace-team"
				    role: "ACE team"
				    source: "Synthetic test register v1"
				    status: PLACEHOLDER
				    openItem: OPEN-038
				"""));

		assertThat(errors(placeholder)).isEmpty();
		assertThat(warnings(placeholder))
			.containsExactly("owner @scb-ace/ace-team is a placeholder for ACE team (OPEN-038)");

		List<CodeOwnersValidator.Finding> confirmed = validate(repo, codeOwners, register(dir, """
				owners:
				  - handle: "@scb-ace/ace-team"
				    role: "ACE team"
				    source: "Synthetic test register v1"
				    status: CONFIRMED
				    openItem: OPEN-038
				"""));

		assertThat(errors(confirmed)).isEmpty();
		assertThat(warnings(confirmed)).isEmpty();
		assertThat(infos(confirmed)).isEmpty();
	}

	@Test
	void registerProblemsFailClosed(@TempDir Path dir) throws IOException {
		Path repo = repository(dir);
		file(repo, "x/keep.txt");
		Path codeOwners = codeOwners(dir, """
				[Recovery module]
				/x/ @scb-ace/ace-team
				""");

		assertThat(errors(validate(repo, codeOwners, dir.resolve("missing-register.yaml"))))
			.containsExactly("register: codeowners-register.yaml not found");

		Files.createDirectories(dir.resolve("directory-register.yaml"));
		assertThat(errors(validate(repo, codeOwners, dir.resolve("directory-register.yaml"))).get(0))
			.startsWith("register: codeowners-register.yaml is not readable: ");

		assertThat(errors(validate(repo, codeOwners, register(dir, "owners: ["))).get(0))
			.startsWith("register: invalid YAML: ");

		assertThat(errors(validate(repo, codeOwners, register(dir, "- not\n- a\n- map\n"))))
			.containsExactly("register: root is not a map");

		assertThat(errors(validate(repo, codeOwners, register(dir, "reservedPatterns: []\n"))))
			.containsExactly("register: owners is missing");

		assertThat(errors(validate(repo, codeOwners, register(dir, "owners:\n  - just text\n"))))
			.containsExactly("register: owners[0] is not a map");

		assertThat(errors(validate(repo, codeOwners, register(dir, """
				owners: []
				reservedPatterns:
				  - just text
				""")))).containsExactly("register: reservedPatterns[0] is not a map");

		assertThat(errors(validate(repo, codeOwners, register(dir, """
				owners: []
				reservedPatterns:
				  - pattern: "/x/"
				""")))).containsExactly("register: reservedPatterns[0] field basis is missing");
	}

	@Test
	void duplicateSectionNameIsRejected(@TempDir Path dir) throws IOException {
		Path repo = repository(dir);
		file(repo, ".gitlab/CODEOWNERS");
		file(repo, "x/keep.txt");
		Path mixedCase = codeOwners(dir, """
				[Code owners control]
				/.gitlab/CODEOWNERS @scb-ace/ace-team
				[code owners CONTROL]
				/.gitlab/CODEOWNERS @scb-ace/ace-team
				""");

		assertThat(errors(validate(repo, mixedCase, register(dir))))
			.containsExactly("line 3: duplicate section code owners CONTROL");

		Path trailingSpace = codeOwners(dir, """
				[Recovery module]
				/x/ @scb-ace/techx-recovery-tech-leads
				[Recovery module ]
				/x/ @scb-ace/techx-recovery-tech-leads
				""");

		assertThat(errors(validate(repo, trailingSpace, register(dir))))
			.containsExactly("line 3: duplicate section Recovery module");

		Path distinct = codeOwners(dir, """
				[Recovery module]
				/x/ @scb-ace/techx-recovery-tech-leads
				[Recovery tests]
				/x/ @scb-ace/techx-recovery-tech-leads
				""");

		assertThat(errors(validate(repo, distinct, register(dir)))).isEmpty();
	}

	@Test
	void emptyOwnerListStillChecksEveryOwner(@TempDir Path dir) throws IOException {
		// Ponytail review Must 1 / security F6: an empty register must fail closed, not accept any team.
		Path repo = repository(dir);
		file(repo, "x/keep.txt");
		Path codeOwners = codeOwners(dir, """
				[Recovery module]
				/x/ @scb-ace/ace-team
				""");

		List<CodeOwnersValidator.Finding> findings = validate(repo, codeOwners, register(dir, "owners: []\n"));

		assertThat(errors(findings)).containsExactly("line 2: owner @scb-ace/ace-team not found");
		assertThat(CodeOwnersValidator.failed(findings)).isTrue();
	}

	@Test
	void dotSegmentPatternsAreRejected(@TempDir Path dir) throws IOException {
		// Ponytail review Nice 2 / security F7: GitLab never matches a dot segment, so V9 must not pass it.
		Path repo = repository(dir);
		file(repo, "x/keep.txt");
		file(repo, "AGENTS.md");
		Path codeOwners = codeOwners(dir, """
				[Recovery module]
				/backend/../x/ @scb-ace/techx-recovery-tech-leads
				/./AGENTS.md @scb-ace/techx-recovery-tech-leads
				/x/.. @scb-ace/techx-recovery-tech-leads
				""");

		assertThat(errors(validate(repo, codeOwners, register(dir)))).containsExactly(
				"line 2: unsupported pattern /backend/../x/",
				"line 3: unsupported pattern /./AGENTS.md",
				"line 4: unsupported pattern /x/..");
	}

	@Test
	void emptySegmentAndColonPatternsAreRejected(@TempDir Path dir) throws IOException {
		// Code gate CODE1-001 / security F7: "//" never matches on GitLab, and "//" or ":" can name a folder outside the checkout.
		Path repo = repository(dir);
		file(repo, "backend/src/keep.txt");
		file(repo, "x/keep.txt");
		Path codeOwners = codeOwners(dir, """
				[Recovery module]
				/backend//src/ @scb-ace/techx-recovery-tech-leads
				//Windows/ @scb-ace/techx-recovery-tech-leads
				/C:/Windows/ @scb-ace/techx-recovery-tech-leads
				/x/keep:txt @scb-ace/techx-recovery-tech-leads
				""");

		assertThat(errors(validate(repo, codeOwners, register(dir)))).containsExactly(
				"line 2: unsupported pattern /backend//src/",
				"line 3: unsupported pattern //Windows/",
				"line 4: unsupported pattern /C:/Windows/",
				"line 5: unsupported pattern /x/keep:txt");
	}

	@Test
	void patternResolvingOutsideTheRootMatchesNoFile(@TempDir Path dir) throws IOException {
		// Code gate CODE1-001 / security F7: V9 counts only files under the repository root.
		Path repo = repository(dir);
		file(repo, "x/keep.txt");
		file(dir, "outside/keep.txt");
		file(dir, "outside.txt");

		assertThat(CodeOwnersValidator.matchesAFile(repo, "/x/")).isTrue();
		assertThat(CodeOwnersValidator.matchesAFile(repo, "/x/keep.txt")).isTrue();
		assertThat(CodeOwnersValidator.matchesAFile(repo, "/../outside/")).isFalse();
		assertThat(CodeOwnersValidator.matchesAFile(repo, "/../outside.txt")).isFalse();
	}

	@Test
	void noHigherPrecedenceCodeOwnersFileExists() {
		// Security F1: GitLab reads /CODEOWNERS, then /docs/CODEOWNERS, before /.gitlab/CODEOWNERS.
		Path root = CodeOwnersValidator.repositoryRoot();

		assertThat(root.resolve("CODEOWNERS")).doesNotExist();
		assertThat(root.resolve("docs/CODEOWNERS")).doesNotExist();
	}

	@Test
	void liveFileAndRegisterPass() {
		Path root = CodeOwnersValidator.repositoryRoot();

		List<CodeOwnersValidator.Finding> findings = validate(root, root.resolve(".gitlab/CODEOWNERS"),
				root.resolve(".gitlab/codeowners-register.yaml"));

		assertThat(errors(findings)).isEmpty();
		assertThat(CodeOwnersValidator.failed(findings)).isFalse();
		assertThat(warnings(findings)).containsExactlyInAnyOrder(
				"line 7: reserved pattern " + COMMON_PATTERN
						+ " matches no file (BR3; DL05; RWB-TE-001 common root th.co.scb.ace.demo.common; OPEN-024)",
				"line 39: reserved pattern /CODEOWNERS matches no file (" + PRECEDENCE_BASIS + ")",
				"line 40: reserved pattern /docs/CODEOWNERS matches no file (" + PRECEDENCE_BASIS + ")",
				"line 46: reserved pattern /CODEOWNERS matches no file (" + PRECEDENCE_BASIS + ")",
				"line 47: reserved pattern /docs/CODEOWNERS matches no file (" + PRECEDENCE_BASIS + ")",
				"owner @role-placeholder/solution-architect-with-tech-leads is a placeholder for"
						+ " Repository standards file owner: solution architect with the tech leads (OPEN-038)",
				"owner @role-placeholder/techx-devops-with-scb-it is a placeholder for"
						+ " Pipeline gates owner: TechX DevOps with SCB IT (OPEN-038)");
		assertThat(infos(findings)).containsExactly(
				"owner " + RECOVERY_TEAM + " is assumed (OPEN-038)",
				"owner " + ACE_TEAM + " is assumed (OPEN-038)");
	}

	private static List<CodeOwnersValidator.Finding> validate(Path repo, Path codeOwners, Path register) {
		return CodeOwnersValidator.validate(repo, codeOwners, register);
	}

	private static Path repository(Path dir) throws IOException {
		return Files.createDirectories(dir.resolve("repo"));
	}

	private static Path codeOwners(Path dir, String content) throws IOException {
		Path file = dir.resolve("CODEOWNERS");
		Files.writeString(file, content);
		return file;
	}

	private static Path register(Path dir) throws IOException {
		return register(dir, REGISTER);
	}

	private static Path register(Path dir, String content) throws IOException {
		Path file = dir.resolve("codeowners-register.yaml");
		Files.writeString(file, content);
		return file;
	}

	private static Path file(Path root, String relative) throws IOException {
		Path target = root.resolve(relative);
		Files.createDirectories(target.getParent());
		Files.writeString(target, "synthetic fixture\n");
		return target;
	}

	private static List<String> errors(List<CodeOwnersValidator.Finding> findings) {
		return messages(findings, CodeOwnersValidator.Level.ERROR);
	}

	private static List<String> warnings(List<CodeOwnersValidator.Finding> findings) {
		return messages(findings, CodeOwnersValidator.Level.WARNING);
	}

	private static List<String> infos(List<CodeOwnersValidator.Finding> findings) {
		return messages(findings, CodeOwnersValidator.Level.INFO);
	}

	private static List<String> messages(List<CodeOwnersValidator.Finding> findings,
			CodeOwnersValidator.Level level) {
		return findings.stream()
			.filter(finding -> finding.level() == level)
			.map(CodeOwnersValidator.Finding::message)
			.toList();
	}
}
