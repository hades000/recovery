package th.co.scb.ace.demo.recovery.integration.internal;

import org.springframework.boot.context.properties.EnableConfigurationProperties;
import org.springframework.context.annotation.Configuration;
import org.springframework.jdbc.core.JdbcTemplate;
import org.springframework.security.access.prepost.PreAuthorize;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

import th.co.scb.ace.demo.recovery.integration.flags.api.RecoveryFlags;

/**
 * Capability area PLATFORM, operation READ_INFO. Reports the environment, the flags and what the
 * service identity can see in the database: the {@code v_ace_*} view count proves the ADR-010
 * read boundary is in place, because {@code information_schema} lists only granted objects.
 */
@RestController
@RequestMapping("/api/recovery/v1/platform")
class PlatformInfoController {

	private final PlatformInfoProperties properties;
	private final RecoveryFlags flags;
	private final JdbcTemplate jdbc;

	PlatformInfoController(PlatformInfoProperties properties, RecoveryFlags flags, JdbcTemplate jdbc) {
		this.properties = properties;
		this.flags = flags;
		this.jdbc = jdbc;
	}

	@GetMapping("/info")
	@PreAuthorize("isAuthenticated()") // PLATFORM.READ_INFO: any signed-in Workbench user
	PlatformInfo info() {
		String schema = properties.schema();
		Integer views = jdbc.queryForObject("""
				SELECT count(*) FROM information_schema.views
				WHERE table_schema = ? AND table_name LIKE 'v\\_ace\\_%'""", Integer.class, schema);
		Integer tables = jdbc.queryForObject("""
				SELECT count(*) FROM information_schema.tables
				WHERE table_schema = ? AND table_type = 'BASE TABLE'""", Integer.class, schema);
		Integer publicTables = jdbc.queryForObject("""
				SELECT count(*) FROM information_schema.tables WHERE table_schema = 'public'""", Integer.class);
		return new PlatformInfo("ace-recovery", properties.environment(), flags,
				new DatabaseView(schema, tables, views, publicTables));
	}

	record PlatformInfo(String service, String environment, RecoveryFlags flags, DatabaseView database) {
	}

	@Configuration(proxyBeanMethods = false)
	@EnableConfigurationProperties(PlatformInfoProperties.class)
	static class Registration {
	}

	/** {@code visiblePublicTables} must be 0: the service identity has no privilege in public. */
	record DatabaseView(String schema, Integer recoveryTables, Integer aceViews, Integer visiblePublicTables) {
	}
}
