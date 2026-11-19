package th.co.scb.ace.demo.recovery.architecture.migration;

import java.util.List;

/**
 * SPEC-RWB-E1-044-005, -010 (ASM-E044-05): the lint lists <em>every</em> folder entry. The
 * {@code .sql} entries are parsed; every other entry name is handed to the folder hook, which is
 * how {@code notes.txt} reaches L-NAME.
 */
public record FolderContext(List<ParsedMigrationFile> parsedFiles, List<String> otherEntries) {

	public FolderContext {
		parsedFiles = List.copyOf(parsedFiles);
		otherEntries = List.copyOf(otherEntries);
	}
}
