package th.co.scb.ace.demo.recovery.architecture.migration;

import java.io.IOException;
import java.io.UncheckedIOException;
import java.nio.file.Files;
import java.nio.file.Path;
import java.util.ArrayList;
import java.util.Comparator;
import java.util.LinkedHashSet;
import java.util.List;
import java.util.stream.Stream;

/**
 * SPEC-RWB-E1-044-004, -010, -016 (T-044-01 to T-044-07, -20 to -22): scan one folder and return
 * every finding.
 *
 * <p>The folder is listed entry by entry. Each {@code .sql} entry is parsed once and every other
 * entry name reaches {@link FolderContext}, so a {@code notes.txt} is reported by {@code L-NAME}
 * (ASM-E044-05). An entry that cannot be read fails closed with an {@link UncheckedIOException} that
 * names it; it is never skipped silently.
 */
public final class MigrationLint {

	private MigrationLint() {
	}

	public static List<MigrationFinding> lint(Path folder) {
		List<Path> entries = list(folder);
		List<ParsedMigrationFile> parsedFiles = new ArrayList<>();
		List<String> otherEntries = new ArrayList<>();
		for (Path entry : entries) {
			String name = entry.getFileName().toString();
			if (name.endsWith(".sql")) {
				parsedFiles.add(parse(entry, name));
			}
			else {
				otherEntries.add(name);
			}
		}
		FolderContext context = new FolderContext(parsedFiles, otherEntries);
		List<MigrationFinding> findings = new ArrayList<>();
		for (MigrationRule rule : MigrationRules.all()) {
			findings.addAll(rule.checkFolder(context));
			for (ParsedMigrationFile file : parsedFiles) {
				findings.addAll(rule.check(file, context));
			}
		}
		return List.copyOf(new LinkedHashSet<>(findings));
	}

	private static List<Path> list(Path folder) {
		try (Stream<Path> stream = Files.list(folder)) {
			return stream.sorted(Comparator.comparing(path -> path.getFileName().toString())).toList();
		}
		catch (IOException ex) {
			throw new UncheckedIOException("cannot list migration folder " + folder, ex);
		}
	}

	private static ParsedMigrationFile parse(Path entry, String name) {
		try {
			return MigrationLexer.parse(entry);
		}
		catch (IOException ex) {
			throw new UncheckedIOException("cannot read migration " + name, ex);
		}
	}

}
