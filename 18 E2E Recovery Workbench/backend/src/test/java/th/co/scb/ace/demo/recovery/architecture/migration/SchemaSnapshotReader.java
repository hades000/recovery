package th.co.scb.ace.demo.recovery.architecture.migration;

import java.sql.Connection;
import java.sql.PreparedStatement;
import java.sql.ResultSet;
import java.sql.SQLException;
import java.util.ArrayList;
import java.util.LinkedHashMap;
import java.util.LinkedHashSet;
import java.util.List;
import java.util.Map;
import java.util.Set;

import th.co.scb.ace.demo.recovery.architecture.migration.SchemaSnapshot.ColumnSnapshot;
import th.co.scb.ace.demo.recovery.architecture.migration.SchemaSnapshot.TableSnapshot;
import th.co.scb.ace.demo.recovery.architecture.migration.SchemaSnapshot.ViewSnapshot;

/**
 * SPEC-RWB-E1-044-012: read one schema's catalog into a {@link SchemaSnapshot}. Only {@link #read}
 * touches a database; {@link #fromRows} is the pure mapping T-044-19 exercises.
 */
public final class SchemaSnapshotReader {

	private static final String COLUMNS = "select c.relname, a.attname, "
			+ "pg_catalog.format_type(a.atttypid, a.atttypmod), a.attnotnull "
			+ "from pg_catalog.pg_attribute a "
			+ "join pg_catalog.pg_class c on c.oid = a.attrelid "
			+ "join pg_catalog.pg_namespace n on n.oid = c.relnamespace "
			+ "where n.nspname = ? and a.attnum > 0 and not a.attisdropped "
			+ "and c.relkind in ('r', 'p', 'v', 'm', 'f') and c.relname <> ?";

	private SchemaSnapshotReader() {
	}

	/** One catalog row per table. */
	public record TableRow(String name) {
	}

	/** One catalog row per column. */
	public record ColumnRow(String table, String column, String dataType, boolean nullable) {
	}

	/** One catalog row per constraint. */
	public record ConstraintRow(String table, String name) {
	}

	/** One catalog row per index. */
	public record IndexRow(String table, String name) {
	}

	/** One catalog row per view column. */
	public record ViewColumnRow(String view, String column) {
	}

	public static SchemaSnapshot fromRows(List<TableRow> tables, List<ColumnRow> columns,
			List<ConstraintRow> constraints, List<IndexRow> indexes, List<ViewColumnRow> viewColumns) {
		Map<String, Set<String>> viewColumnsByName = new LinkedHashMap<>();
		for (ViewColumnRow row : viewColumns) {
			viewColumnsByName.computeIfAbsent(row.view(), name -> new LinkedHashSet<>()).add(row.column());
		}
		Set<ViewSnapshot> views = new LinkedHashSet<>();
		viewColumnsByName.forEach((name, columnsOfView) -> views.add(new ViewSnapshot(name, columnsOfView)));

		Map<String, Map<String, ColumnSnapshot>> columnsByTable = new LinkedHashMap<>();
		for (ColumnRow row : columns) {
			columnsByTable.computeIfAbsent(row.table(), name -> new LinkedHashMap<>())
				.put(row.column(), new ColumnSnapshot(row.column(), row.dataType(), row.nullable()));
		}
		Map<String, Set<String>> constraintsByTable = new LinkedHashMap<>();
		for (ConstraintRow row : constraints) {
			constraintsByTable.computeIfAbsent(row.table(), name -> new LinkedHashSet<>()).add(row.name());
		}
		Map<String, Set<String>> indexesByTable = new LinkedHashMap<>();
		for (IndexRow row : indexes) {
			indexesByTable.computeIfAbsent(row.table(), name -> new LinkedHashSet<>()).add(row.name());
		}

		Set<TableSnapshot> tableSnapshots = new LinkedHashSet<>();
		for (TableRow row : tables) {
			tableSnapshots.add(new TableSnapshot(row.name(),
					columnsByTable.getOrDefault(row.name(), Map.of()),
					constraintsByTable.getOrDefault(row.name(), Set.of()),
					indexesByTable.getOrDefault(row.name(), Set.of())));
		}
		return new SchemaSnapshot(tableSnapshots, views);
	}

	/**
	 * Read one schema's catalog. {@code historyTable} is Flyway's own bookkeeping: it is not a
	 * Workbench object, and its generated constraint names embed OIDs, so it is left out of the
	 * comparison. The caller passes the one constant from the Flyway configuration (SEC/ponytail 5).
	 */
	public static SchemaSnapshot read(Connection connection, String schema, String historyTable) throws SQLException {
		List<TableRow> tables = new ArrayList<>();
		try (PreparedStatement statement = connection.prepareStatement(
				"select table_name from information_schema.tables where table_schema = ? and table_type = 'BASE TABLE' "
						+ "and table_name <> ?")) {
			statement.setString(1, schema);
			statement.setString(2, historyTable);
			try (ResultSet rows = statement.executeQuery()) {
				while (rows.next()) {
					tables.add(new TableRow(rows.getString(1)));
				}
			}
		}
		List<ColumnRow> columns = new ArrayList<>();
		try (PreparedStatement statement = connection.prepareStatement(COLUMNS)) {
			statement.setString(1, schema);
			statement.setString(2, historyTable);
			try (ResultSet rows = statement.executeQuery()) {
				while (rows.next()) {
					columns.add(new ColumnRow(rows.getString(1), rows.getString(2), rows.getString(3),
							!rows.getBoolean(4)));
				}
			}
		}
		List<ConstraintRow> constraints = new ArrayList<>();
		try (PreparedStatement statement = connection.prepareStatement(
				"select tc.table_name, tc.constraint_name from information_schema.table_constraints tc "
						+ "where tc.table_schema = ? and tc.table_name <> ?")) {
			statement.setString(1, schema);
			statement.setString(2, historyTable);
			try (ResultSet rows = statement.executeQuery()) {
				while (rows.next()) {
					constraints.add(new ConstraintRow(rows.getString(1), rows.getString(2)));
				}
			}
		}
		List<IndexRow> indexes = new ArrayList<>();
		try (PreparedStatement statement = connection
			.prepareStatement("select tablename, indexname from pg_indexes where schemaname = ? and tablename <> ?")) {
			statement.setString(1, schema);
			statement.setString(2, historyTable);
			try (ResultSet rows = statement.executeQuery()) {
				while (rows.next()) {
					indexes.add(new IndexRow(rows.getString(1), rows.getString(2)));
				}
			}
		}
		List<ViewColumnRow> viewColumns = new ArrayList<>();
		try (PreparedStatement statement = connection.prepareStatement(
				"select c.table_name, c.column_name from information_schema.columns c "
						+ "where c.table_schema = ? and c.table_name in "
						+ "(select v.table_name from information_schema.views v where v.table_schema = ?)")) {
			statement.setString(1, schema);
			statement.setString(2, schema);
			try (ResultSet rows = statement.executeQuery()) {
				while (rows.next()) {
					viewColumns.add(new ViewColumnRow(rows.getString(1), rows.getString(2)));
				}
			}
		}
		return fromRows(tables, columns, constraints, indexes, viewColumns);
	}

}
