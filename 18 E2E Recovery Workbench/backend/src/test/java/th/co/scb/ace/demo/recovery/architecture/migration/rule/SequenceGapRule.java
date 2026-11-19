package th.co.scb.ace.demo.recovery.architecture.migration.rule;

import java.util.ArrayList;
import java.util.List;
import java.util.TreeSet;
import java.util.stream.Collectors;

import th.co.scb.ace.demo.recovery.architecture.migration.FolderContext;
import th.co.scb.ace.demo.recovery.architecture.migration.MigrationFinding;
import th.co.scb.ace.demo.recovery.architecture.migration.MigrationRule;
import th.co.scb.ace.demo.recovery.architecture.migration.ParsedMigrationFile;

/**
 * SPEC-RWB-E1-044-005 (T-044-01): sequences are contiguous {@code V0001..N}. The comparison uses
 * the <em>distinct</em> sequence numbers, so a duplicate is reported once by
 * {@link SequenceDuplicateRule} and never also as a gap (PA-E044-06).
 */
public final class SequenceGapRule implements MigrationRule {

	@Override
	public String ruleId() {
		return "L-SEQ-GAP";
	}

	@Override
	public List<MigrationFinding> check(ParsedMigrationFile file, FolderContext folder) {
		return List.of();
	}

	@Override
	public List<MigrationFinding> checkFolder(FolderContext folder) {
		TreeSet<Integer> sequences = folder.parsedFiles()
			.stream()
			.map(ParsedMigrationFile::sequence)
			.filter(sequence -> sequence >= 0)
			.collect(Collectors.toCollection(TreeSet::new));
		if (sequences.isEmpty()) {
			return List.of();
		}
		List<MigrationFinding> findings = new ArrayList<>();
		if (sequences.first() < 1) {
			String version = String.format("V%04d", sequences.first());
			findings.add(new MigrationFinding(ruleId(), version, 0, version, "sequence must start at V0001"));
		}
		int highest = sequences.last();
		for (int expected = 1; expected <= highest; expected++) {
			if (!sequences.contains(expected)) {
				String version = String.format("V%04d", expected);
				findings.add(new MigrationFinding(ruleId(), version, 0, version, "sequence gap, expected " + version));
			}
		}
		return findings;
	}

}
