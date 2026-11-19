package th.co.scb.ace.demo.recovery.testsupport;

import java.io.IOException;
import java.util.List;

import org.springframework.boot.env.YamlPropertySourceLoader;
import org.springframework.boot.test.context.runner.ApplicationContextRunner;
import org.springframework.context.annotation.AnnotationConfigApplicationContext;
import org.springframework.core.env.PropertySource;
import org.springframework.core.env.StandardEnvironment;
import org.springframework.core.io.ClassPathResource;

/**
 * RWB-TE-001 SPEC-023 (T-TE001-12, PLAN-012): reads {@code application.yaml} on an environment with
 * no system environment or system-property source, so the {@code ${RWB_...:default}} placeholders
 * resolve to the file defaults under both {@code ./gradlew test} and {@code scripts/dev.ps1 test}
 * (which imports {@code .env}).
 */
public final class ApplicationYamlEnvironment {

	private ApplicationYamlEnvironment() {
	}

	public static StandardEnvironment isolated() {
		StandardEnvironment environment = new StandardEnvironment();
		environment.getPropertySources().remove(StandardEnvironment.SYSTEM_ENVIRONMENT_PROPERTY_SOURCE_NAME);
		environment.getPropertySources().remove(StandardEnvironment.SYSTEM_PROPERTIES_PROPERTY_SOURCE_NAME);
		try {
			List<PropertySource<?>> loaded = new YamlPropertySourceLoader().load("application.yaml",
					new ClassPathResource("application.yaml"));
			loaded.forEach(environment.getPropertySources()::addLast);
		}
		catch (IOException ex) {
			throw new IllegalStateException("application.yaml is not readable", ex);
		}
		return environment;
	}

	public static ApplicationContextRunner runner() {
		return new ApplicationContextRunner(() -> {
			AnnotationConfigApplicationContext context = new AnnotationConfigApplicationContext();
			context.setEnvironment(isolated());
			return context;
		});
	}
}
