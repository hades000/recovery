package th.co.scb.ace.demo.recovery.architecture.codeowners;

import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Path;
import java.util.ArrayList;
import java.util.HashSet;
import java.util.List;
import java.util.Map;
import java.util.Set;

import org.yaml.snakeyaml.LoaderOptions;
import org.yaml.snakeyaml.Yaml;
import org.yaml.snakeyaml.constructor.SafeConstructor;
import org.yaml.snakeyaml.error.YAMLException;

/**
 * RWB-TE-002 SPEC-009 (TASK-01, TASK-04): the owner register {@code .gitlab/codeowners-register.yaml},
 * the only local source of valid owners. Fails closed: every defect is a problem text (V11), a malformed
 * owner is left out and the rest is still read. Unknown keys are ignored (PA-11). Test scope only.
 */
final class OwnerRegister {

	private static final List<String> OWNER_FIELDS = List.of("handle", "role", "source", "status", "openItem");

	private static final List<String> RESERVED_FIELDS = List.of("pattern", "basis");

	private static final Set<String> STATUSES = Set.of("ASSUMED", "PLACEHOLDER", "CONFIRMED");

	/** One owner row: five fields, no person, no membership, no e-mail. */
	record Owner(String handle, String role, String source, String status, String openItem) {
	}

	/** A reserved pattern: listed in the file but allowed to match no file (V10). */
	record ReservedPattern(String pattern, String basis) {
	}

	private final List<Owner> owners = new ArrayList<>();

	private final List<ReservedPattern> reservedPatterns = new ArrayList<>();

	private final List<String> problems = new ArrayList<>();

	private OwnerRegister() {
	}

	static OwnerRegister read(Path file) {
		OwnerRegister register = new OwnerRegister();
		if (!Files.exists(file)) {
			register.problems.add("codeowners-register.yaml not found");
			return register;
		}
		String text;
		try {
			text = Files.readString(file);
		}
		catch (IOException e) {
			register.problems.add("codeowners-register.yaml is not readable: " + e);
			return register;
		}
		Object root;
		try {
			root = new Yaml(new SafeConstructor(new LoaderOptions())).load(text);
		}
		catch (YAMLException e) {
			register.problems.add("invalid YAML: " + e.getMessage().lines().findFirst().orElse(""));
			return register;
		}
		if (!(root instanceof Map<?, ?> map)) {
			register.problems.add("root is not a map");
			return register;
		}
		if (!(map.get("owners") instanceof List<?> ownerRows)) {
			register.problems.add("owners is missing");
		}
		else {
			register.readOwners(ownerRows);
		}
		if (map.get("reservedPatterns") instanceof List<?> reservedRows) {
			register.readReserved(reservedRows);
		}
		return register;
	}

	private void readOwners(List<?> rows) {
		Set<String> handles = new HashSet<>();
		for (int i = 0; i < rows.size(); i++) {
			List<String> values = fields("owners", i, rows.get(i), OWNER_FIELDS);
			if (values == null) {
				continue;
			}
			if (!STATUSES.contains(values.get(3))) {
				problems.add("owners[" + i + "] status " + values.get(3)
						+ " is not one of ASSUMED, PLACEHOLDER, CONFIRMED");
			}
			else if (!handles.add(values.get(0))) {
				problems.add("owners[" + i + "] handle " + values.get(0) + " is listed twice");
			}
			else {
				owners.add(new Owner(values.get(0), values.get(1), values.get(2), values.get(3), values.get(4)));
			}
		}
	}

	private void readReserved(List<?> rows) {
		for (int i = 0; i < rows.size(); i++) {
			List<String> values = fields("reservedPatterns", i, rows.get(i), RESERVED_FIELDS);
			if (values != null) {
				reservedPatterns.add(new ReservedPattern(values.get(0), values.get(1)));
			}
		}
	}

	/** The named fields of one row in order, or {@code null} after recording why the row is rejected. */
	private List<String> fields(String list, int index, Object row, List<String> names) {
		if (!(row instanceof Map<?, ?> map)) {
			problems.add(list + "[" + index + "] is not a map");
			return null;
		}
		List<String> values = new ArrayList<>();
		for (String name : names) {
			Object value = map.get(name);
			if (value == null || value.toString().isBlank()) {
				problems.add(list + "[" + index + "] field " + name + " is missing");
				return null;
			}
			values.add(value.toString());
		}
		return values;
	}

	List<Owner> owners() {
		return List.copyOf(owners);
	}

	List<ReservedPattern> reservedPatterns() {
		return List.copyOf(reservedPatterns);
	}

	List<String> problems() {
		return List.copyOf(problems);
	}
}
