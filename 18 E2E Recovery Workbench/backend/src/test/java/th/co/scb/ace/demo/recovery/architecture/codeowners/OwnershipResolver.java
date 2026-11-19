package th.co.scb.ace.demo.recovery.architecture.codeowners;

import java.util.Collection;
import java.util.LinkedHashMap;
import java.util.LinkedHashSet;
import java.util.Map;
import java.util.Set;

/**
 * RWB-TE-002 SPEC-007 (TASK-01, TASK-04): pure resolver. For each path and each section, the owners of
 * the last matching entry in that section; union across paths, file order for sections. Test scope
 * only.
 */
final class OwnershipResolver {

	private OwnershipResolver() {
	}

	static Map<String, Set<String>> resolve(CodeOwnersFile file, Collection<String> changedPaths) {
		Map<String, Set<String>> result = new LinkedHashMap<>();
		for (CodeOwnersFile.Section section : file.sections()) {
			for (String changed : changedPaths) {
				String path = changed.replace('\\', '/').replaceFirst("^\\./", "");
				CodeOwnersFile.Entry last = null;
				for (CodeOwnersFile.Entry entry : file.entries()) {
					if (entry.section().equals(section.name()) && matches(entry.pattern(), path)) {
						last = entry;
					}
				}
				if (last != null) {
					result.computeIfAbsent(section.name(), name -> new LinkedHashSet<>()).addAll(last.owners());
				}
			}
		}
		return result;
	}

	/** Directory pattern ({@code /a/}): path starts with it; file pattern: path equals it; leading {@code /} dropped. */
	static boolean matches(String pattern, String path) {
		String relative = pattern.replaceFirst("^/", "");
		return pattern.endsWith("/") ? path.startsWith(relative) : path.equals(relative);
	}
}
