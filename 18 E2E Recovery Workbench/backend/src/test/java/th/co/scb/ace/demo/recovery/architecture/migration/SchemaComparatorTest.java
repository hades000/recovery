package th.co.scb.ace.demo.recovery.architecture.migration;

import static org.assertj.core.api.Assertions.assertThat;

import java.util.LinkedHashMap;
import java.util.List;
import java.util.Map;
import java.util.Set;
import java.util.stream.Collectors;
import java.util.stream.Stream;

import org.junit.jupiter.api.Test;

import th.co.scb.ace.demo.recovery.architecture.migration.SchemaSnapshot.ColumnSnapshot;
import th.co.scb.ace.demo.recovery.architecture.migration.SchemaSnapshot.TableSnapshot;
import th.co.scb.ace.demo.recovery.architecture.migration.SchemaSnapshot.ViewSnapshot;

/**
 * SPEC-RWB-E1-044-012 (T-044-19): the pure schema comparator and the catalog-row mapping that needs
 * no database. A difference is reported in the {@code MSG-P3-016 schema=recovery object=<path>}
 * format; equal snapshots give none.
 */
class SchemaComparatorTest {

	@Test
	void equalSnapshotsGiveNoDifference() {
		SchemaSnapshot left = snapshot(table("queue", column("id", "bigint", false)),
				table("timer", column("id", "bigint", false)));

		assertThat(SchemaComparator.compare(left, left)).isEmpty();
		assertThat(SchemaComparator.compare(left, snapshot(table("queue", column("id", "bigint", false)),
				table("timer", column("id", "bigint", false))))).isEmpty();
	}

	@Test
	void addedMissingAndChangedColumnEachGiveOneDifference() {
		SchemaSnapshot left = snapshot(table("queue", column("id", "bigint", false),
				column("team_code", "text", true)));
		SchemaSnapshot added = snapshot(table("queue", column("id", "bigint", false),
				column("team_code", "text", true), column("note_x", "text", true)));
		SchemaSnapshot missing = snapshot(table("queue", column("id", "bigint", false)));
		SchemaSnapshot changed = snapshot(table("queue", column("id", "bigint", false),
				column("team_code", "varchar(8)", true)));
		SchemaSnapshot nullability = snapshot(table("queue", column("id", "bigint", false),
				column("team_code", "text", false)));

		assertThat(SchemaComparator.compare(left, added)).singleElement()
			.isEqualTo(new SchemaDifference(SchemaDifference.Kind.ADDED, "recovery.queue.note_x"));
		assertThat(SchemaComparator.compare(left, missing)).singleElement()
			.isEqualTo(new SchemaDifference(SchemaDifference.Kind.MISSING, "recovery.queue.team_code"));
		assertThat(SchemaComparator.compare(left, changed)).singleElement()
			.isEqualTo(new SchemaDifference(SchemaDifference.Kind.CHANGED, "recovery.queue.team_code"));
		assertThat(SchemaComparator.compare(left, nullability)).singleElement()
			.isEqualTo(new SchemaDifference(SchemaDifference.Kind.CHANGED, "recovery.queue.team_code"));
	}

	@Test
	void constraintIndexAndViewEachGiveOneDifference() {
		SchemaSnapshot left = new SchemaSnapshot(
				Set.of(new TableSnapshot("queue", Map.of("id", column("id", "bigint", false)),
						Set.of("pk_queue", "uq_queue_team"), Set.of("ix_queue_team"))),
				Set.of(new ViewSnapshot("v_queue", Set.of("id"))));
		SchemaSnapshot right = new SchemaSnapshot(
				Set.of(new TableSnapshot("queue", Map.of("id", column("id", "bigint", false)),
						Set.of("pk_queue"), Set.of("ix_queue_team", "ix_queue_note"))),
				Set.of(new ViewSnapshot("v_queue", Set.of("id", "team_code"))));

		assertThat(SchemaComparator.compare(left, right)).containsExactly(
				new SchemaDifference(SchemaDifference.Kind.MISSING, "recovery.queue.uq_queue_team"),
				new SchemaDifference(SchemaDifference.Kind.ADDED, "recovery.ix_queue_note"),
				new SchemaDifference(SchemaDifference.Kind.CHANGED, "recovery.v_queue"));
	}

	@Test
	void aWholeTableOrViewIsReportedByItsName() {
		SchemaSnapshot left = snapshot(table("queue", column("id", "bigint", false)));
		SchemaSnapshot right = snapshot(table("queue", column("id", "bigint", false)),
				table("timer", column("id", "bigint", false)));
		SchemaSnapshot withView = new SchemaSnapshot(Set.of(table("queue", column("id", "bigint", false))),
				Set.of(new ViewSnapshot("v_queue", Set.of("id"))));

		assertThat(SchemaComparator.compare(left, right)).containsExactly(
				new SchemaDifference(SchemaDifference.Kind.ADDED, "recovery.timer"));
		assertThat(SchemaComparator.compare(left, withView)).containsExactly(
				new SchemaDifference(SchemaDifference.Kind.ADDED, "recovery.v_queue"));
		assertThat(SchemaComparator.compare(right, left)).containsExactly(
				new SchemaDifference(SchemaDifference.Kind.MISSING, "recovery.timer"));
	}

	@Test
	void aTypeLengthPrecisionOrEnumChangeIsADifference() {
		SchemaSnapshot base = snapshot(table("queue", column("code", "character varying(8)", true),
				column("amount", "numeric(10,2)", true), column("mood", "mood_old", true)));

		assertThat(SchemaComparator.compare(base, snapshot(table("queue", column("code", "character varying(50)", true),
				column("amount", "numeric(10,2)", true), column("mood", "mood_old", true))))).containsExactly(
						new SchemaDifference(SchemaDifference.Kind.CHANGED, "recovery.queue.code"));
		assertThat(SchemaComparator.compare(base, snapshot(table("queue", column("code", "character varying(8)", true),
				column("amount", "numeric(12,2)", true), column("mood", "mood_old", true))))).containsExactly(
						new SchemaDifference(SchemaDifference.Kind.CHANGED, "recovery.queue.amount"));
		assertThat(SchemaComparator.compare(base, snapshot(table("queue", column("code", "character varying(8)", true),
				column("amount", "numeric(10,2)", true), column("mood", "mood_new", true))))).containsExactly(
						new SchemaDifference(SchemaDifference.Kind.CHANGED, "recovery.queue.mood"));
	}

	@Test
	void aDifferenceFormatsAsMessageP3() {
		assertThat(new SchemaDifference(SchemaDifference.Kind.ADDED, "recovery.queue.note_x").format())
			.isEqualTo("MSG-P3-016 schema=recovery object=recovery.queue.note_x");
	}

	@Test
	void snapshotReaderMapsCatalogRows() {
		SchemaSnapshot snapshot = SchemaSnapshotReader.fromRows(List.of(new SchemaSnapshotReader.TableRow("queue"),
				new SchemaSnapshotReader.TableRow("timer")),
				List.of(new SchemaSnapshotReader.ColumnRow("queue", "id", "bigint", false),
						new SchemaSnapshotReader.ColumnRow("queue", "team_code", "text", true),
						new SchemaSnapshotReader.ColumnRow("timer", "id", "bigint", false)),
				List.of(new SchemaSnapshotReader.ConstraintRow("queue", "pk_queue")),
				List.of(new SchemaSnapshotReader.IndexRow("queue", "ix_queue_team")),
				List.of(new SchemaSnapshotReader.ViewColumnRow("v_queue", "id")));

		assertThat(snapshot.tables()).extracting(TableSnapshot::name).containsExactlyInAnyOrder("queue", "timer");
		TableSnapshot queue = snapshot.tables().stream().filter(t -> t.name().equals("queue")).findFirst().orElseThrow();
		assertThat(queue.columns()).containsEntry("team_code", new ColumnSnapshot("team_code", "text", true));
		assertThat(queue.constraints()).containsExactly("pk_queue");
		assertThat(queue.indexes()).containsExactly("ix_queue_team");
		assertThat(snapshot.views()).containsExactly(new ViewSnapshot("v_queue", Set.of("id")));
	}

	private static SchemaSnapshot snapshot(TableSnapshot... tables) {
		return new SchemaSnapshot(Stream.of(tables).collect(Collectors.toSet()), Set.of());
	}

	private static TableSnapshot table(String name, ColumnSnapshot... columns) {
		Map<String, ColumnSnapshot> byName = new LinkedHashMap<>();
		for (ColumnSnapshot column : columns) {
			byName.put(column.name(), column);
		}
		return new TableSnapshot(name, byName, Set.of(), Set.of());
	}

	private static ColumnSnapshot column(String name, String dataType, boolean nullable) {
		return new ColumnSnapshot(name, dataType, nullable);
	}

}
