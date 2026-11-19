package th.co.scb.ace.demo.recovery.architecture.migration;

import java.util.ArrayList;
import java.util.List;
import java.util.Map;
import java.util.Objects;
import java.util.Set;
import java.util.TreeMap;
import java.util.TreeSet;

/**
 * SPEC-RWB-E1-044-012 (T-044-19, -15): pure comparison of two {@link SchemaSnapshot}s. The right
 * side is described relative to the left: an object only on the right is {@code ADDED}, one only on
 * the left is {@code MISSING}, and a column whose type or nullability differs is {@code CHANGED}.
 */
public final class SchemaComparator {

	private SchemaComparator() {
	}

	public static List<SchemaDifference> compare(SchemaSnapshot left, SchemaSnapshot right) {
		List<SchemaDifference> differences = new ArrayList<>();
		Map<String, SchemaSnapshot.TableSnapshot> leftTables = byName(left);
		Map<String, SchemaSnapshot.TableSnapshot> rightTables = byName(right);
		for (String name : union(leftTables, rightTables)) {
			SchemaSnapshot.TableSnapshot expected = leftTables.get(name);
			SchemaSnapshot.TableSnapshot actual = rightTables.get(name);
			if (expected == null) {
				differences.add(new SchemaDifference(SchemaDifference.Kind.ADDED, "recovery." + name));
			}
			else if (actual == null) {
				differences.add(new SchemaDifference(SchemaDifference.Kind.MISSING, "recovery." + name));
			}
			else {
				compareTable(name, expected, actual, differences);
			}
		}
		compareViews(left, right, differences);
		return List.copyOf(differences);
	}

	private static void compareTable(String table, SchemaSnapshot.TableSnapshot expected,
			SchemaSnapshot.TableSnapshot actual, List<SchemaDifference> differences) {
		TreeSet<String> columns = new TreeSet<>(expected.columns().keySet());
		columns.addAll(actual.columns().keySet());
		for (String column : columns) {
			SchemaSnapshot.ColumnSnapshot expectedColumn = expected.columns().get(column);
			SchemaSnapshot.ColumnSnapshot actualColumn = actual.columns().get(column);
			String path = "recovery." + table + "." + column;
			if (expectedColumn == null) {
				differences.add(new SchemaDifference(SchemaDifference.Kind.ADDED, path));
			}
			else if (actualColumn == null) {
				differences.add(new SchemaDifference(SchemaDifference.Kind.MISSING, path));
			}
			else if (!Objects.equals(expectedColumn.dataType(), actualColumn.dataType())
					|| expectedColumn.nullable() != actualColumn.nullable()) {
				differences.add(new SchemaDifference(SchemaDifference.Kind.CHANGED, path));
			}
		}
		compareNames(expected.constraints(), actual.constraints(), "recovery." + table + ".",
				differences);
		compareNames(expected.indexes(), actual.indexes(), "recovery.", differences);
	}

	private static void compareNames(Set<String> expected, Set<String> actual, String prefix,
			List<SchemaDifference> differences) {
		TreeSet<String> names = new TreeSet<>(expected);
		names.addAll(actual);
		for (String name : names) {
			if (!expected.contains(name)) {
				differences.add(new SchemaDifference(SchemaDifference.Kind.ADDED, prefix + name));
			}
			else if (!actual.contains(name)) {
				differences.add(new SchemaDifference(SchemaDifference.Kind.MISSING, prefix + name));
			}
		}
	}

	private static void compareViews(SchemaSnapshot left, SchemaSnapshot right, List<SchemaDifference> differences) {
		Map<String, SchemaSnapshot.ViewSnapshot> leftViews = new TreeMap<>();
		left.views().forEach(view -> leftViews.put(view.name(), view));
		Map<String, SchemaSnapshot.ViewSnapshot> rightViews = new TreeMap<>();
		right.views().forEach(view -> rightViews.put(view.name(), view));
		for (String name : union(leftViews, rightViews)) {
			SchemaSnapshot.ViewSnapshot expected = leftViews.get(name);
			SchemaSnapshot.ViewSnapshot actual = rightViews.get(name);
			if (expected == null) {
				differences.add(new SchemaDifference(SchemaDifference.Kind.ADDED, "recovery." + name));
			}
			else if (actual == null) {
				differences.add(new SchemaDifference(SchemaDifference.Kind.MISSING, "recovery." + name));
			}
			else if (!expected.columns().equals(actual.columns())) {
				differences.add(new SchemaDifference(SchemaDifference.Kind.CHANGED, "recovery." + name));
			}
		}
	}

	private static Map<String, SchemaSnapshot.TableSnapshot> byName(SchemaSnapshot snapshot) {
		Map<String, SchemaSnapshot.TableSnapshot> byName = new TreeMap<>();
		snapshot.tables().forEach(table -> byName.put(table.name(), table));
		return byName;
	}

	private static <T> TreeSet<String> union(Map<String, T> left, Map<String, T> right) {
		TreeSet<String> names = new TreeSet<>(left.keySet());
		names.addAll(right.keySet());
		return names;
	}

}
