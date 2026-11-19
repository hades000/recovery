package th.co.scb.ace.demo.recovery.architecture.codeowners;

import java.io.IOException;
import java.io.UncheckedIOException;
import java.nio.charset.StandardCharsets;
import java.nio.file.Files;
import java.nio.file.NoSuchFileException;
import java.nio.file.Path;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.List;
import java.util.regex.Matcher;
import java.util.regex.Pattern;

/**
 * RWB-TE-002 SPEC-001, SPEC-007, SPEC-008 (TASK-01, TASK-04): parsed {@code .gitlab/CODEOWNERS} in
 * GitLab section format, with 1-based line numbers. Test scope only: no main-source class, no jar
 * entry.
 */
final class CodeOwnersFile {

	private static final Pattern HEADER = Pattern.compile("^\\[([^\\[\\]]+)\\]$");

	static final String SYNTAX_ERROR = "syntax error";

	static final String ORPHAN = "entry outside a section";

	/** A section header {@code [Name]} on its own line. {@code name} is trimmed, {@code line} 1-based. */
	record Section(String name, int line) {
	}

	/**
	 * One entry {@code pattern owner...}. {@code section} is {@code null} for an orphan entry (V2), which
	 * is reported and not kept.
	 */
	record Entry(String pattern, List<String> owners, int line, String section) {
	}

	/** A syntax problem: V1 ({@code syntax error}) or V2 ({@code entry outside a section}). */
	record Problem(int line, String reason) {
	}

	private final List<Section> sections;

	private final List<Entry> entries;

	private final List<Problem> problems;

	private CodeOwnersFile(List<Section> sections, List<Entry> entries, List<Problem> problems) {
		this.sections = List.copyOf(sections);
		this.entries = List.copyOf(entries);
		this.problems = List.copyOf(problems);
	}

	static CodeOwnersFile parse(Path file) {
		try {
			return parse(Files.readAllLines(file, StandardCharsets.UTF_8));
		}
		catch (NoSuchFileException e) {
			throw new IllegalStateException("CODEOWNERS not found: " + file, e);
		}
		catch (IOException e) {
			throw new UncheckedIOException(e);
		}
	}

	static CodeOwnersFile parse(List<String> lines) {
		List<Section> sections = new ArrayList<>();
		List<Entry> entries = new ArrayList<>();
		List<Problem> problems = new ArrayList<>();
		String current = null;
		for (int i = 0; i < lines.size(); i++) {
			int line = i + 1;
			String text = lines.get(i).strip();
			if (text.isEmpty() || text.startsWith("#")) {
				continue;
			}
			if (text.startsWith("[")) {
				Matcher header = HEADER.matcher(text);
				if (header.matches()) {
					current = header.group(1).strip();
					sections.add(new Section(current, line));
				}
				else {
					problems.add(new Problem(line, SYNTAX_ERROR));
				}
			}
			else if (text.startsWith("^")) {
				problems.add(new Problem(line, SYNTAX_ERROR));
			}
			else if (current == null) {
				problems.add(new Problem(line, ORPHAN));
			}
			else {
				List<String> tokens = Arrays.asList(text.split("\\s+"));
				entries.add(new Entry(tokens.get(0), List.copyOf(tokens.subList(1, tokens.size())), line, current));
			}
		}
		return new CodeOwnersFile(sections, entries, problems);
	}

	List<Section> sections() {
		return sections;
	}

	List<Entry> entries() {
		return entries;
	}

	List<Problem> problems() {
		return problems;
	}
}
