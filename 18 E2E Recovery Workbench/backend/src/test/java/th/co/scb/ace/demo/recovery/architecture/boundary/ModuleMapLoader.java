package th.co.scb.ace.demo.recovery.architecture.boundary;

import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Path;
import java.util.ArrayList;
import java.util.LinkedHashMap;
import java.util.LinkedHashSet;
import java.util.List;
import java.util.Map;
import java.util.Set;
import java.util.regex.Pattern;

import org.yaml.snakeyaml.LoaderOptions;
import org.yaml.snakeyaml.Yaml;
import org.yaml.snakeyaml.constructor.SafeConstructor;
import org.yaml.snakeyaml.error.YAMLException;

/**
 * RWB-TE-001 SPEC-003 (BR6): reads the module map into {@link ModuleMap}. Every malformed map is
 * refused with {@code <file>: <field path>: <problem>}; the optional {@code sourceViews} key is
 * carried unvalidated for RWB-E1-069. No package literal: the root comes from the map.
 */
public final class ModuleMapLoader {

	private static final Pattern CODE = Pattern.compile("^(P([1-9]|10)|S[1-9])$");

	private static final Pattern NAME = Pattern.compile("^[a-z][a-z0-9]*$");

	private static final Pattern PACKAGE = Pattern.compile("^[a-z][a-z0-9]*(\\.[a-z][a-z0-9]*)*$");

	private static final Pattern JAVA_NAME = Pattern.compile("^[A-Za-z_$][A-Za-z0-9_$]*(\\.[A-Za-z_$][A-Za-z0-9_$]*)*$");

	private static final Set<String> TOP_LEVEL_KEYS = Set.of("rootPackage", "modules", "external", "clientLibraries",
			"sourceViews");

	private static final Set<String> MODULE_KEYS = Set.of("code", "name", "published", "clientPackages");

	private static final Set<String> EXTERNAL_KEYS = Set.of("name", "rootPackage", "published");

	private static final Set<String> EXTERNAL_NAMES = Set.of("common", "collection");

	private ModuleMapLoader() {
	}

	public static ModuleMap load(Path file) {
		String source = file.getFileName().toString();
		Map<String, Object> root = mapping(parse(source, file), "$", source);

		for (String key : root.keySet()) {
			if (!TOP_LEVEL_KEYS.contains(key)) {
				throw fail(source, key, "unknown key");
			}
		}

		String rootPackage = requiredString(root, "rootPackage", "rootPackage", source);
		if (!PACKAGE.matcher(rootPackage).matches()) {
			throw fail(source, "rootPackage", "does not match " + PACKAGE.pattern());
		}
		List<ModuleMap.Module> modules = modules(list(root, "modules", "modules", source, true), source);
		List<ModuleMap.External> external = external(list(root, "external", "external", source, true), source);
		List<String> clientLibraries = clientLibraries(
				list(root, "clientLibraries", "clientLibraries", source, true), source);

		return new ModuleMap(source, rootPackage, modules, external, clientLibraries, root.get("sourceViews"));
	}

	private static List<ModuleMap.Module> modules(List<Object> values, String source) {
		List<ModuleMap.Module> modules = new ArrayList<>();
		Set<String> codes = new LinkedHashSet<>();
		Set<String> names = new LinkedHashSet<>();
		for (int i = 0; i < values.size(); i++) {
			String path = "modules[" + i + "]";
			Map<String, Object> module = mapping(values.get(i), path, source);
			for (String key : module.keySet()) {
				if (!MODULE_KEYS.contains(key)) {
					throw fail(source, path + "." + key, "unknown key");
				}
			}
			String code = requiredString(module, "code", path + ".code", source);
			if (!CODE.matcher(code).matches()) {
				throw fail(source, path + ".code", "does not match " + CODE.pattern());
			}
			if (!codes.add(code)) {
				throw fail(source, path + ".code", "duplicate value " + code);
			}
			String name = requiredString(module, "name", path + ".name", source);
			if (!NAME.matcher(name).matches()) {
				throw fail(source, path + ".name", "does not match " + NAME.pattern());
			}
			if (!names.add(name)) {
				throw fail(source, path + ".name", "duplicate value " + name);
			}
			List<String> published = packages(module, "published", path, source, true);
			List<String> clientPackages = packages(module, "clientPackages", path, source, false);
			modules.add(new ModuleMap.Module(code, name, published, clientPackages));
		}
		return modules;
	}

	private static List<ModuleMap.External> external(List<Object> values, String source) {
		List<ModuleMap.External> external = new ArrayList<>();
		Set<String> names = new LinkedHashSet<>();
		for (int i = 0; i < values.size(); i++) {
			String path = "external[" + i + "]";
			Map<String, Object> entry = mapping(values.get(i), path, source);
			for (String key : entry.keySet()) {
				if (!EXTERNAL_KEYS.contains(key)) {
					throw fail(source, path + "." + key, "unknown key");
				}
			}
			String name = requiredString(entry, "name", path + ".name", source);
			if (!EXTERNAL_NAMES.contains(name)) {
				throw fail(source, path + ".name", "does not match " + EXTERNAL_NAMES);
			}
			if (!names.add(name)) {
				throw fail(source, path + ".name", "duplicate value " + name);
			}
			String rootPackage = requiredString(entry, "rootPackage", path + ".rootPackage", source);
			if (!PACKAGE.matcher(rootPackage).matches()) {
				throw fail(source, path + ".rootPackage", "does not match " + PACKAGE.pattern());
			}
			List<String> published = packages(entry, "published", path, source, true);
			external.add(new ModuleMap.External(name, rootPackage, published));
		}
		if (!names.equals(EXTERNAL_NAMES)) {
			throw fail(source, "external", "must list exactly common and collection");
		}
		return external;
	}

	private static List<String> clientLibraries(List<Object> values, String source) {
		List<String> entries = new ArrayList<>();
		Set<String> seen = new LinkedHashSet<>();
		for (int i = 0; i < values.size(); i++) {
			String entry = string(values.get(i), "clientLibraries[" + i + "]", source);
			if (!JAVA_NAME.matcher(entry).matches()) {
				throw fail(source, "clientLibraries[" + i + "]", "does not match " + JAVA_NAME.pattern());
			}
			if (!seen.add(entry)) {
				throw fail(source, "clientLibraries[" + i + "]", "duplicate value " + entry);
			}
			entries.add(entry);
		}
		return entries;
	}

	private static List<String> packages(Map<String, Object> owner, String key, String ownerPath, String source,
			boolean forbidInternal) {
		List<Object> values = list(owner, key, ownerPath + "." + key, source, forbidInternal);
		List<String> packages = new ArrayList<>();
		Set<String> seen = new LinkedHashSet<>();
		for (int i = 0; i < values.size(); i++) {
			String path = ownerPath + "." + key + "[" + i + "]";
			String entry = string(values.get(i), path, source);
			if (!PACKAGE.matcher(entry).matches()) {
				throw fail(source, path, "does not match " + PACKAGE.pattern());
			}
			if (forbidInternal && (entry.equals("internal") || entry.startsWith("internal."))) {
				throw fail(source, path, "must not be internal or under internal");
			}
			// CONF-TE001-01: a published list is unique (spec field matrix); clientPackages has no such rule.
			if (forbidInternal && !seen.add(entry)) {
				throw fail(source, path, "duplicate value " + entry);
			}
			packages.add(entry);
		}
		return packages;
	}

	private static Object parse(String source, Path file) {
		String text;
		try {
			text = Files.readString(file);
		}
		catch (IOException ex) {
			throw fail(source, "$", "cannot read " + file);
		}
		try {
			LoaderOptions options = new LoaderOptions();
			options.setAllowDuplicateKeys(false);
			return new Yaml(new SafeConstructor(options)).load(text);
		}
		catch (YAMLException ex) {
			String message = String.valueOf(ex.getMessage());
			if (message.contains("found duplicate key")) {
				throw fail(source, "$", "duplicate key " + message.substring(message.indexOf("found duplicate key")
						+ "found duplicate key ".length()).split("\\R", 2)[0].trim());
			}
			throw fail(source, "$", "invalid YAML: " + message.split("\\R", 2)[0]);
		}
	}

	private static Map<String, Object> mapping(Object value, String path, String source) {
		if (!(value instanceof Map<?, ?> map)) {
			throw fail(source, path, "must be a mapping");
		}
		Map<String, Object> result = new LinkedHashMap<>();
		for (Map.Entry<?, ?> entry : map.entrySet()) {
			if (!(entry.getKey() instanceof String key)) {
				throw fail(source, path, "must use string keys");
			}
			result.put(key, entry.getValue());
		}
		return result;
	}

	private static String requiredString(Map<String, Object> owner, String key, String path, String source) {
		Object value = owner.get(key);
		if (value == null) {
			throw fail(source, path, "required");
		}
		String text = string(value, path, source);
		if (text.isEmpty()) {
			throw fail(source, path, "required");
		}
		return text;
	}

	private static List<Object> list(Map<String, Object> owner, String key, String path, String source,
			boolean nonEmpty) {
		Object value = owner.get(key);
		if (value == null) {
			throw fail(source, path, "required");
		}
		if (!(value instanceof List<?> list)) {
			throw fail(source, path, "must be a list");
		}
		if (nonEmpty && list.isEmpty()) {
			throw fail(source, path, "required");
		}
		return new ArrayList<>(list);
	}

	private static String string(Object value, String path, String source) {
		if (!(value instanceof String text)) {
			throw fail(source, path, "must be a string");
		}
		return text;
	}

	private static IllegalStateException fail(String source, String path, String problem) {
		return new IllegalStateException(source + ": " + path + ": " + problem);
	}
}
