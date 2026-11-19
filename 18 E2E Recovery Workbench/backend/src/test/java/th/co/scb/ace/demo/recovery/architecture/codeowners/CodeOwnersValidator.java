package th.co.scb.ace.demo.recovery.architecture.codeowners;

import java.io.IOException;
import java.io.UncheckedIOException;
import java.nio.file.Files;
import java.nio.file.Path;
import java.util.ArrayList;
import java.util.Comparator;
import java.util.HashMap;
import java.util.HashSet;
import java.util.List;
import java.util.Locale;
import java.util.Map;
import java.util.Optional;
import java.util.Set;
import java.util.regex.Pattern;
import java.util.stream.Collectors;
import java.util.stream.Stream;

/**
 * RWB-TE-002 SPEC-008 (TASK-01, TASK-04): rules V1-V12 and the placeholder/assumed notes. Collects
 * every finding and fails when any finding is {@link Level#ERROR}. Messages exactly as
 * {@code data-model.md} §1.3. Test scope only.
 */
final class CodeOwnersValidator {

	private static final Pattern TEAM = Pattern.compile("^@[A-Za-z0-9][A-Za-z0-9._-]*/[A-Za-z0-9][A-Za-z0-9._-]*$");

	private static final Pattern UNSUPPORTED = Pattern.compile("[*?\\[!\\\\]");

	/** A ".", ".." or empty path segment, or a ":": GitLab never matches it, and it can name a path off the root (F7). */
	private static final Pattern NON_NORMAL = Pattern.compile("(^|/)\\.{1,2}(/|$)|//|:");

	enum Level {
		ERROR, WARNING, INFO
	}

	/** {@code line} is 0 for a register finding; {@code pattern} and {@code owner} are null when not named. */
	record Finding(Level level, int line, String message, String pattern, String owner) {
	}

	private CodeOwnersValidator() {
	}

	static List<Finding> validate(Path repoRoot, Path codeOwners, Path register) {
		OwnerRegister owners = OwnerRegister.read(register);
		List<Finding> findings = new ArrayList<>();
		for (String problem : owners.problems()) {
			findings.add(new Finding(Level.ERROR, 0, "register: " + problem, null, null));
		}
		if (Files.isRegularFile(codeOwners)) {
			findings.addAll(checkFile(repoRoot, CodeOwnersFile.parse(codeOwners), owners));
		}
		else {
			findings.add(new Finding(Level.ERROR, 0, ".gitlab/CODEOWNERS not found", null, null));
		}
		for (OwnerRegister.Owner owner : owners.owners()) {
			if ("PLACEHOLDER".equals(owner.status())) {
				findings.add(new Finding(Level.WARNING, 0, "owner " + owner.handle() + " is a placeholder for "
						+ owner.role() + " (" + owner.openItem() + ")", null, owner.handle()));
			}
			else if ("ASSUMED".equals(owner.status())) {
				findings.add(new Finding(Level.INFO, 0,
						"owner " + owner.handle() + " is assumed (" + owner.openItem() + ")", null, owner.handle()));
			}
		}
		return List.copyOf(findings);
	}

	private static List<Finding> checkFile(Path root, CodeOwnersFile file, OwnerRegister register) {
		List<Finding> findings = new ArrayList<>();
		for (CodeOwnersFile.Problem problem : file.problems()) {
			findings.add(error(problem.line(), problem.reason(), null, null));
		}
		Set<String> sectionNames = new HashSet<>();
		for (CodeOwnersFile.Section section : file.sections()) {
			if (!sectionNames.add(section.name().toLowerCase(Locale.ROOT))) {
				findings.add(error(section.line(), "duplicate section " + section.name(), null, null));
			}
		}
		Set<String> handles = register.owners().stream().map(OwnerRegister.Owner::handle).collect(Collectors.toSet());
		Map<String, String> reserved = new HashMap<>();
		register.reservedPatterns().forEach(entry -> reserved.put(entry.pattern(), entry.basis()));
		List<CodeOwnersFile.Entry> entries = file.entries();
		Set<String> seen = new HashSet<>();
		for (int i = 0; i < entries.size(); i++) {
			CodeOwnersFile.Entry entry = entries.get(i);
			int line = entry.line();
			String pattern = entry.pattern();
			if (entry.owners().isEmpty()) {
				findings.add(error(line, "pattern " + pattern + " has no owner", pattern, null));
			}
			boolean supported = supported(pattern);
			if (!supported) {
				findings.add(error(line, "unsupported pattern " + pattern, pattern, null));
			}
			// V5 is per section block: a repeated header is V12's finding, not a duplicate pattern (UT-23 B).
			else if (!seen.add(sectionBlock(file, line) + "\n" + pattern)) {
				findings.add(error(line, "duplicate pattern " + pattern + " in section " + entry.section(), pattern,
						null));
			}
			else {
				shadowing(entries, i).ifPresent(later -> findings.add(error(line, "pattern " + pattern
						+ " is shadowed by later pattern " + later + " in section " + entry.section(), pattern, null)));
			}
			for (String owner : entry.owners()) {
				if (!TEAM.matcher(owner).matches()) {
					findings.add(error(line, "owner " + owner + " is not a team", pattern, owner));
				}
				// Fail closed: an empty owner list rejects every owner; a broken register is already an error (V11).
				else if (register.problems().isEmpty() && !handles.contains(owner)) {
					findings.add(error(line, "owner " + owner + " not found", pattern, owner));
				}
			}
			if (supported && !matchesAFile(root, pattern)) {
				if (reserved.containsKey(pattern)) {
					findings.add(new Finding(Level.WARNING, line, "line " + line + ": reserved pattern " + pattern
							+ " matches no file (" + reserved.get(pattern) + ")", pattern, null));
				}
				else {
					findings.add(error(line, "pattern " + pattern + " matches no file", pattern, null));
				}
			}
		}
		findings.sort(Comparator.comparingInt(Finding::line));
		return findings;
	}

	private static Optional<String> shadowing(List<CodeOwnersFile.Entry> entries, int index) {
		CodeOwnersFile.Entry entry = entries.get(index);
		String path = entry.pattern().substring(1);
		return entries.subList(index + 1, entries.size()).stream()
			.filter(later -> later.section().equals(entry.section()))
			.map(CodeOwnersFile.Entry::pattern)
			.filter(later -> supported(later) && later.endsWith("/") && !later.equals(entry.pattern())
					&& path.startsWith(later.substring(1)))
			.findFirst();
	}

	/** The header line of the section block that holds {@code line}. */
	private static int sectionBlock(CodeOwnersFile file, int line) {
		return file.sections().stream().mapToInt(CodeOwnersFile.Section::line).filter(header -> header < line).max()
			.orElse(0);
	}

	private static boolean supported(String pattern) {
		return pattern.startsWith("/") && !UNSUPPORTED.matcher(pattern).find() && !NON_NORMAL.matcher(pattern).find();
	}

	static boolean matchesAFile(Path root, String pattern) {
		Path base = root.toAbsolutePath().normalize();
		Path target = base.resolve(pattern.substring(1)).normalize();
		if (!target.startsWith(base)) {
			return false;
		}
		if (!pattern.endsWith("/")) {
			return Files.isRegularFile(target);
		}
		if (!Files.isDirectory(target)) {
			return false;
		}
		try (Stream<Path> files = Files.walk(target)) {
			return files.anyMatch(Files::isRegularFile);
		}
		catch (IOException e) {
			throw new UncheckedIOException(e);
		}
	}

	private static Finding error(int line, String reason, String pattern, String owner) {
		return new Finding(Level.ERROR, line, "line " + line + ": " + reason, pattern, owner);
	}

	static boolean failed(List<Finding> findings) {
		return findings.stream().anyMatch(finding -> finding.level() == Level.ERROR);
	}

	static Path repositoryRoot() {
		Path root = Path.of("").toAbsolutePath().getParent();
		if (root == null || !Files.isRegularFile(root.resolve(".gitlab-ci.yml"))) {
			throw new IllegalStateException("repository root with .gitlab-ci.yml not found above "
					+ Path.of("").toAbsolutePath());
		}
		return root;
	}
}
