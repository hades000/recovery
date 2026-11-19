package th.co.scb.ace.demo.recovery.architecture.migration;

import java.util.LinkedHashMap;
import java.util.Map;
import java.util.Set;

/** SPEC-RWB-E1-044-012: one recovery schema as a value, for the drift comparison (T-044-19, -15). */
public record SchemaSnapshot(Set<TableSnapshot> tables, Set<ViewSnapshot> views) {

	public SchemaSnapshot {
		tables = Set.copyOf(tables);
		views = Set.copyOf(views);
	}

	/** A table with its columns, constraints and indexes; names are unqualified in schema recovery. */
	public record TableSnapshot(String name, Map<String, ColumnSnapshot> columns, Set<String> constraints,
			Set<String> indexes) {

		public TableSnapshot {
			columns = Map.copyOf(new LinkedHashMap<>(columns));
			constraints = Set.copyOf(constraints);
			indexes = Set.copyOf(indexes);
		}

	}

	/** A column's data type and nullability, as {@code information_schema.columns} reports them. */
	public record ColumnSnapshot(String name, String dataType, boolean nullable) {
	}

	/** A view and its column names. */
	public record ViewSnapshot(String name, Set<String> columns) {

		public ViewSnapshot {
			columns = Set.copyOf(columns);
		}
	}

}
