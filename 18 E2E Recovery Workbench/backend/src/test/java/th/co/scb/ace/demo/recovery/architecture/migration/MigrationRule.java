package th.co.scb.ace.demo.recovery.architecture.migration;

import java.util.List;

/**
 * SPEC-RWB-E1-044-016: one implementation per rule ID, all listed in {@link MigrationRules#all()}.
 * Adding a rule is one new class plus one registry entry; no other rule changes.
 */
public interface MigrationRule {

	String ruleId();

	List<MigrationFinding> check(ParsedMigrationFile file, FolderContext folder);

	/** The folder-level hook: naming rules override it; every other rule returns nothing. */
	default List<MigrationFinding> checkFolder(FolderContext folder) {
		return List.of();
	}
}
