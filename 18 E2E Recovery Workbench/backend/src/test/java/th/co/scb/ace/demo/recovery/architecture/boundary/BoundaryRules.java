package th.co.scb.ace.demo.recovery.architecture.boundary;

import java.util.ArrayList;
import java.util.LinkedHashSet;
import java.util.List;
import java.util.Optional;
import java.util.Set;

import com.tngtech.archunit.core.domain.Dependency;
import com.tngtech.archunit.core.domain.JavaClass;
import com.tngtech.archunit.core.domain.JavaModifier;
import com.tngtech.archunit.core.domain.JavaPackage;
import com.tngtech.archunit.lang.ArchCondition;
import com.tngtech.archunit.lang.ArchRule;
import com.tngtech.archunit.lang.ConditionEvents;
import com.tngtech.archunit.lang.SimpleConditionEvent;
import com.tngtech.archunit.lang.syntax.ArchRuleDefinition;
import jakarta.persistence.Entity;
import org.springframework.data.repository.Repository;
import org.springframework.modulith.NamedInterface;

/**
 * RWB-TE-001 SPEC-004..-010 (BR1..BR6): the map-driven boundary rules. Every rule reports one line
 * per distinct violation with the SPEC-010 text; the map is the only source of module names,
 * packages, published packages, client packages and client libraries.
 */
public final class BoundaryRules {

	private static final String TEMPLATE = "Rule %s broken: %s depends on %s. Use %s.api or an application event.";

	private BoundaryRules() {
	}

	public static List<ArchRule> all(ModuleMap map) {
		return List.of(moduleMap(map), bnd1(map), bnd2(map), bnd4(map), bnd5(map));
	}

	public static ArchRule moduleMap(ModuleMap map) {
		return rule(new ModuleMapCondition(map));
	}

	public static ArchRule bnd1(ModuleMap map) {
		return rule(new ExternalCondition(map, "BND-1", external(map, "collection"))).allowEmptyShould(true);
	}

	public static ArchRule bnd2(ModuleMap map) {
		return rule(new ExternalCondition(map, "BND-2", external(map, "common"))).allowEmptyShould(true);
	}

	public static ArchRule bnd4(ModuleMap map) {
		return rule(new EntityCondition(map));
	}

	public static ArchRule bnd5(ModuleMap map) {
		return rule(new ClientLibraryCondition(map));
	}

	/** A dependency matches when it equals the entry or starts past its dot or dollar boundary. */
	public static boolean matchesClientLibrary(String entry, String className) {
		return className.equals(entry) || className.startsWith(entry + ".") || className.startsWith(entry + "$");
	}

	private static ArchRule rule(ArchCondition<JavaClass> condition) {
		return ArchRuleDefinition.classes().should(condition);
	}

	private static ModuleMap.External external(ModuleMap map, String name) {
		return map.external()
			.stream()
			.filter(entry -> entry.name().equals(name))
			.findFirst()
			.orElseThrow(() -> new IllegalStateException("the map has no external module " + name));
	}

	private static boolean isUnder(String packageName, String root) {
		return packageName.equals(root) || packageName.startsWith(root + ".");
	}

	private static Optional<String> externalName(ModuleMap map, String packageName) {
		return map.external()
			.stream()
			.filter(entry -> isUnder(packageName, entry.rootPackage()))
			.map(ModuleMap.External::name)
			.findFirst();
	}

	/** Base class that reports each distinct message once, in one evaluation (SPEC-010). */
	private abstract static class ReportingCondition extends ArchCondition<JavaClass> {

		private final Set<String> reported = new LinkedHashSet<>();

		ReportingCondition() {
			super("report the boundary violations");
		}

		void report(ConditionEvents events, String message) {
			if (reported.add(message)) {
				events.add(SimpleConditionEvent.violated(this, message));
			}
		}

		String externalOrPackageText(ModuleMap map, JavaClass target) {
			return map.moduleOf(target.getPackageName())
				.map(ModuleMap.Module::name)
				.or(() -> externalName(map, target.getPackageName()))
				.orElse(target.getPackageName());
		}
	}

	/** MAP: every package, published package and module base package agrees with the map. */
	private static final class ModuleMapCondition extends ReportingCondition {

		private final ModuleMap map;

		private final List<JavaClass> imported = new ArrayList<>();

		ModuleMapCondition(ModuleMap map) {
			this.map = map;
		}

		@Override
		public void check(JavaClass type, ConditionEvents events) {
			imported.add(type);
			String packageName = type.getPackageName();
			if (!isUnder(packageName, map.rootPackage())) {
				return;
			}
			boolean packageInfo = type.getSimpleName().equals("package-info");

			if (!packageName.equals(map.rootPackage())) {
				String child = directChild(packageName);
				if (map.modules().stream().noneMatch(module -> map.modulePackage(module).equals(child))) {
					report(events, "package " + child + " is not in the module map");
				}
			}
			if (packageName.equals(map.rootPackage()) && !packageInfo) {
				report(events, "type " + type.getName() + " in root package " + packageName
						+ "; only package-info is allowed");
			}
			Optional<ModuleMap.Module> module = map.moduleOf(packageName);
			if (module.isEmpty()) {
				return;
			}
			String modulePackage = map.modulePackage(module.get());
			JavaPackage javaPackage = type.getPackage();
			Optional<NamedInterface> named = javaPackage.tryGetAnnotationOfType(NamedInterface.class);
			if (named.isPresent()) {
				String relative = packageName.substring(modulePackage.length() + 1);
				if (!module.get().published().contains(relative)) {
					report(events, "package " + packageName
							+ " has @NamedInterface but is not in the published list of module " + module.get().name());
				}
				if (named.get().propagate()) {
					report(events, "@NamedInterface on " + packageName
							+ " must declare propagate = false; list each published sub-package in the module map");
				}
			}
			for (String entry : module.get().published()) {
				if ((modulePackage + "." + entry).equals(packageName) && named.isEmpty()) {
					report(events, "published package " + packageName + " of module " + module.get().name()
							+ " has no @NamedInterface");
				}
			}
			if (packageInfo) {
				return;
			}
			if (type.isAnnotatedWith(NamedInterface.class)) {
				report(events, "type-level @NamedInterface on " + type.getName()
						+ "; declare published packages in package-info and the module map");
			}
			if (packageName.equals(modulePackage) && type.getModifiers().contains(JavaModifier.PUBLIC)) {
				report(events, "public type " + type.getName() + " in module base package " + packageName
						+ "; move it to a published package or internal");
			}
		}

		@Override
		public void finish(ConditionEvents events) {
			for (ModuleMap.Module module : map.modules()) {
				String modulePackage = map.modulePackage(module);
				if (imported.stream().noneMatch(type -> isUnder(type.getPackageName(), modulePackage))) {
					report(events, "module " + module.name() + " (" + module.code() + ") in the module map has no package "
							+ modulePackage);
				}
			}
		}

		private String directChild(String packageName) {
			String rest = packageName.substring(map.rootPackage().length() + 1);
			int dot = rest.indexOf('.');
			return map.rootPackage() + "." + (dot < 0 ? rest : rest.substring(0, dot));
		}
	}

	/** BND-1 and BND-2: only the external module's published packages may be used. */
	private static final class ExternalCondition extends ReportingCondition {

		private final ModuleMap map;

		private final String code;

		private final ModuleMap.External external;

		ExternalCondition(ModuleMap map, String code, ModuleMap.External external) {
			this.map = map;
			this.code = code;
			this.external = external;
		}

		@Override
		public void check(JavaClass origin, ConditionEvents events) {
			if (!isUnder(origin.getPackageName(), map.rootPackage())) {
				return;
			}
			for (Dependency dependency : origin.getDirectDependenciesFromSelf()) {
				JavaClass target = dependency.getTargetClass();
				if (!isUnder(target.getPackageName(), external.rootPackage())) {
					continue;
				}
				boolean published = external.published()
					.stream()
					.anyMatch(entry -> target.getPackageName().equals(external.rootPackage() + "." + entry));
				if (published) {
					continue;
				}
				report(events, TEMPLATE.formatted(code, origin.getName(), target.getName(),
						external.name()));
			}
		}
	}

	/** BND-4: an entity or repository may only be used inside its own recovery module. */
	private static final class EntityCondition extends ReportingCondition {

		private final ModuleMap map;

		EntityCondition(ModuleMap map) {
			this.map = map;
		}

		@Override
		public void check(JavaClass origin, ConditionEvents events) {
			if (!isUnder(origin.getPackageName(), map.rootPackage())) {
				return;
			}
			Optional<ModuleMap.Module> originModule = map.moduleOf(origin.getPackageName());
			for (Dependency dependency : origin.getDirectDependenciesFromSelf()) {
				JavaClass target = dependency.getTargetClass();
				if (!isEntityOrRepository(target)) {
					continue;
				}
				Optional<ModuleMap.Module> targetModule = map.moduleOf(target.getPackageName());
				if (originModule.isPresent() && targetModule.isPresent()
						&& originModule.get().equals(targetModule.get())) {
					continue;
				}
				report(events, TEMPLATE.formatted("BND-4", origin.getName(), target.getName(),
						externalOrPackageText(map, target)));
			}
		}

		private static boolean isEntityOrRepository(JavaClass type) {
			if (type.getPackageName().startsWith("org.springframework.data")) {
				return false;
			}
			return type.isAnnotatedWith(Entity.class) || type.isAssignableTo(Repository.class);
		}
	}

	/** BND-5: a client library is only used in a client package of the using module (SPEC-009). */
	private static final class ClientLibraryCondition extends ReportingCondition {

		private final ModuleMap map;

		ClientLibraryCondition(ModuleMap map) {
			this.map = map;
		}

		@Override
		public void check(JavaClass origin, ConditionEvents events) {
			if (!isUnder(origin.getPackageName(), map.rootPackage())) {
				return;
			}
			Optional<ModuleMap.Module> originModule = map.moduleOf(origin.getPackageName());
			boolean allowed = originModule.isPresent() && originModule.get()
				.clientPackages()
				.stream()
				.anyMatch(entry -> isUnder(origin.getPackageName(),
						map.modulePackage(originModule.get()) + "." + entry));
			if (allowed) {
				return;
			}
			String module = map.modules()
				.stream()
				.filter(candidate -> candidate.code().equals("P2"))
				.map(ModuleMap.Module::name)
				.findFirst()
				.orElseGet(() -> originModule.map(ModuleMap.Module::name).orElse(origin.getPackageName()));
			for (Dependency dependency : origin.getDirectDependenciesFromSelf()) {
				JavaClass target = dependency.getTargetClass();
				boolean matches = map.clientLibraries()
					.stream()
					.anyMatch(entry -> matchesClientLibrary(entry, target.getName()));
				if (matches) {
					report(events, TEMPLATE.formatted("BND-5", origin.getName(), target.getName(), module));
				}
			}
		}
	}
}
