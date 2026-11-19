package th.co.scb.ace.demo.recovery.architecture.migration;

import java.util.List;

import th.co.scb.ace.demo.recovery.architecture.migration.rule.FixLine2Rule;
import th.co.scb.ace.demo.recovery.architecture.migration.rule.FixNoBaseRule;
import th.co.scb.ace.demo.recovery.architecture.migration.rule.ForeignKeyOutsideRule;
import th.co.scb.ace.demo.recovery.architecture.migration.rule.GrantRule;
import th.co.scb.ace.demo.recovery.architecture.migration.rule.HeaderMultiRule;
import th.co.scb.ace.demo.recovery.architecture.migration.rule.HeaderRule;
import th.co.scb.ace.demo.recovery.architecture.migration.rule.KeyDuplicateRule;
import th.co.scb.ace.demo.recovery.architecture.migration.rule.LexRule;
import th.co.scb.ace.demo.recovery.architecture.migration.rule.LiteralSchemaRule;
import th.co.scb.ace.demo.recovery.architecture.migration.rule.NameRule;
import th.co.scb.ace.demo.recovery.architecture.migration.rule.RepeatableRule;
import th.co.scb.ace.demo.recovery.architecture.migration.rule.SearchPathRule;
import th.co.scb.ace.demo.recovery.architecture.migration.rule.SequenceDuplicateRule;
import th.co.scb.ace.demo.recovery.architecture.migration.rule.SequenceGapRule;
import th.co.scb.ace.demo.recovery.architecture.migration.rule.UndoRule;

/**
 * SPEC-RWB-E1-044-016: the one ordered registry. Adding a rule is one new class plus one entry
 * here; no other rule changes.
 */
public final class MigrationRules {

	private static final List<MigrationRule> ALL = List.of(new NameRule(), new UndoRule(), new RepeatableRule(),
			new SequenceGapRule(), new SequenceDuplicateRule(), new HeaderRule(), new HeaderMultiRule(),
			new KeyDuplicateRule(), new FixLine2Rule(), new FixNoBaseRule(), new SearchPathRule(),
			new LiteralSchemaRule(), new ForeignKeyOutsideRule(), new GrantRule(), new LexRule());

	private MigrationRules() {
	}

	public static List<MigrationRule> all() {
		return ALL;
	}

}
