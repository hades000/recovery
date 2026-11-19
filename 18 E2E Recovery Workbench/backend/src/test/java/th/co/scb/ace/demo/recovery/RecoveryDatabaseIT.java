package th.co.scb.ace.demo.recovery;

import static org.assertj.core.api.Assertions.assertThat;
import static org.assertj.core.api.Assertions.assertThatThrownBy;

import java.nio.file.Path;
import java.sql.DriverManager;
import java.sql.SQLException;
import java.time.Duration;

import org.junit.jupiter.api.Tag;
import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.context.SpringBootTest;
import org.springframework.jdbc.core.JdbcTemplate;
import org.springframework.test.context.DynamicPropertyRegistry;
import org.springframework.test.context.DynamicPropertySource;
import org.testcontainers.containers.wait.strategy.Wait;
import org.testcontainers.junit.jupiter.Container;
import org.testcontainers.junit.jupiter.Testcontainers;
import org.testcontainers.postgresql.PostgreSQLContainer;
import org.testcontainers.utility.MountableFile;

/**
 * Builds the ace database exactly as the local stack does (infra/postgres) and checks the
 * ADR-010 boundary, the recovery Flyway bean and the ADR-009 append-only decision log, as the
 * recovery service identity. Runs in {@code recoveryIntegrationTest}; fails without Docker.
 */
@Tag("recovery-it")
@Testcontainers
@SpringBootTest(properties = { "rwb.p3.temporal=false", "rwb.p3.drools=false", "rwb.environment=DEV" })
class RecoveryDatabaseIT {

	private static final Path INFRA = Path.of("..", "infra", "postgres").toAbsolutePath().normalize();

	@Container
	static final PostgreSQLContainer POSTGRES = new PostgreSQLContainer("postgres:16.16-alpine")
			.withEnv("RWB_MIGRATOR_PASSWORD", "it-migrator")
			.withEnv("RECOVERY_SVC_PASSWORD", "it-recovery")
			.withEnv("TEMPORAL_SVC_PASSWORD", "it-temporal")
			.withEnv("RWB_ACE_TIER2_PROBE", "true")
			.withEnv("RWB_LOAD_REFERENCE_SCHEMA", "true")
			.withCopyFileToContainer(MountableFile.forHostPath(INFRA.resolve("init")), "/docker-entrypoint-initdb.d")
			.withCopyFileToContainer(MountableFile.forHostPath(INFRA.resolve("schema")), "/schema")
			.waitingFor(Wait.forLogMessage(".*database system is ready to accept connections.*\\s", 2)
					.withStartupTimeout(Duration.ofMinutes(4)));

	static String aceUrl() {
		return "jdbc:postgresql://" + POSTGRES.getHost() + ":" + POSTGRES.getMappedPort(5432) + "/ace";
	}

	@DynamicPropertySource
	static void database(DynamicPropertyRegistry registry) {
		registry.add("spring.datasource.url", RecoveryDatabaseIT::aceUrl);
		registry.add("spring.datasource.username", () -> "recovery_svc");
		registry.add("spring.datasource.password", () -> "it-recovery");
		registry.add("rwb.flyway.url", RecoveryDatabaseIT::aceUrl);
		registry.add("rwb.flyway.user", () -> "rwb_migrator");
		registry.add("rwb.flyway.password", () -> "it-migrator");
		// Azurite development account; no call is made unless a document is written.
		registry.add("rwb.blob.connection-string", () -> "UseDevelopmentStorage=true");
	}

	@Autowired
	JdbcTemplate jdbc;

	@Test
	void serviceSeesAllThirtyAceViewsAndNoPublicTable() {
		assertThat(jdbc.queryForObject("SELECT current_user", String.class)).isEqualTo("recovery_svc");
		assertThat(jdbc.queryForObject("""
				SELECT count(*) FROM information_schema.views
				WHERE table_schema = 'recovery' AND table_name LIKE 'v\\_ace\\_%'""", Integer.class)).isEqualTo(30);
		assertThat(jdbc.queryForObject(
				"SELECT count(*) FROM information_schema.tables WHERE table_schema = 'public'", Integer.class)).isZero();
		assertThat(jdbc.queryForObject("SELECT count(*) FROM v_ace_account", Integer.class)).isZero();
	}

	@Test
	void directReadOfAnAceTableFailsInTheCatalog() {
		assertThatThrownBy(() -> jdbc.queryForObject("SELECT count(*) FROM public.account", Integer.class))
				.hasRootCauseInstanceOf(SQLException.class)
				.rootCause().satisfies(ex -> assertThat(((SQLException) ex).getSQLState()).isEqualTo("42501"));
	}

	/** SELECT only: no write grant on any of the 30 views, and a write is refused. */
	@Test
	void aceViewsAreReadOnlyForTheService() {
		assertThat(jdbc.queryForObject("""
				SELECT count(*) FROM pg_views v
				WHERE v.schemaname = 'recovery' AND v.viewname LIKE 'v\\_ace\\_%'
				  AND has_table_privilege('recovery_svc', format('recovery.%I', v.viewname), 'SELECT')
				  AND NOT has_table_privilege('recovery_svc', format('recovery.%I', v.viewname), 'INSERT, UPDATE, DELETE, TRUNCATE')
				  AND v.viewowner = 'ace_view_owner'""", Integer.class)).isEqualTo(30);
		// 42501 (no privilege) or 55000 (view not updatable): either way the write never happens.
		assertThatThrownBy(() -> jdbc.update("DELETE FROM v_ace_account"))
				.rootCause().satisfies(ex -> assertThat(((SQLException) ex).getSQLState()).isIn("42501", "55000"));
	}

	@Test
	void recoveryFlywayBaselinedItsOwnHistoryTable() {
		assertThat(jdbc.queryForObject(
				"SELECT count(*) FROM flyway_schema_history_recovery WHERE version = '0'", Integer.class)).isEqualTo(1);
	}

	@Test
	void decisionLogIsAppendOnly() {
		jdbc.update("""
				INSERT INTO decision_log_entry (decision_code, inputs_ref, final_call, prev_hash, entry_hash, chain_seq)
				VALUES ('IT', 'it://synthetic', 'IT', repeat('0', 64), repeat('1', 64), 1)""");
		assertThatThrownBy(() -> jdbc.update("UPDATE decision_log_entry SET final_call = 'CHANGED'"))
				.isNotNull();
		assertThatThrownBy(() -> jdbc.update("DELETE FROM decision_log_entry")).isNotNull();
	}

	@Test
	void temporalAndRecoveryIdentitiesAreSeparated() {
		String temporalUrl = aceUrl().replace("/ace", "/temporal");
		assertThatThrownBy(() -> DriverManager.getConnection(aceUrl(), "temporal_svc", "it-temporal").close())
				.isInstanceOf(SQLException.class);
		assertThatThrownBy(() -> DriverManager.getConnection(temporalUrl, "recovery_svc", "it-recovery").close())
				.isInstanceOf(SQLException.class);
	}
}
