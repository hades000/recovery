package th.co.scb.ace.demo.recovery.casewf.migration;

import static org.assertj.core.api.Assertions.assertThat;
import static org.assertj.core.api.Assertions.assertThatThrownBy;

import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Path;
import java.nio.file.StandardOpenOption;
import java.sql.Connection;
import java.sql.DriverManager;
import java.sql.ResultSet;
import java.sql.SQLException;
import java.sql.Statement;
import java.time.Duration;
import java.util.ArrayList;
import java.util.List;
import java.util.concurrent.CountDownLatch;
import java.util.concurrent.ExecutorService;
import java.util.concurrent.Executors;
import java.util.concurrent.Future;
import java.util.concurrent.TimeUnit;
import java.util.concurrent.atomic.AtomicInteger;
import java.util.stream.Stream;

import javax.sql.DataSource;

import org.flywaydb.core.Flyway;
import org.flywaydb.core.api.FlywayException;
import org.junit.jupiter.api.Tag;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.io.TempDir;
import org.slf4j.LoggerFactory;
import org.testcontainers.containers.wait.strategy.Wait;
import org.testcontainers.junit.jupiter.Container;
import org.testcontainers.junit.jupiter.Testcontainers;
import org.testcontainers.postgresql.PostgreSQLContainer;
import org.testcontainers.utility.MountableFile;

import org.springframework.boot.jdbc.autoconfigure.DataSourceProperties;
import org.springframework.boot.test.context.runner.ApplicationContextRunner;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import org.springframework.jdbc.datasource.DriverManagerDataSource;

import ch.qos.logback.classic.Logger;
import ch.qos.logback.classic.spi.ILoggingEvent;
import ch.qos.logback.core.read.ListAppender;

import th.co.scb.ace.demo.recovery.architecture.migration.SchemaComparator;
import th.co.scb.ace.demo.recovery.architecture.migration.SchemaDifference;
import th.co.scb.ace.demo.recovery.architecture.migration.SchemaSnapshot;
import th.co.scb.ace.demo.recovery.architecture.migration.SchemaSnapshotReader;

/**
 * SPEC-RWB-E1-044-011, -012, -013, -017 (T-044-10..-18): the production Flyway bean's behaviour
 * against the local init's database. One class, tagged {@code recovery-it}, so
 * {@code recoveryIntegrationTest} runs it and it fails rather than skips without Docker.
 *
 * <p>Every case builds Flyway through {@link RecoveryFlywayConfig#recoveryFlyway} and starts from a
 * fresh database created with {@code CREATE DATABASE <name> TEMPLATE ace}; only
 * {@code rwb.flyway.location} points at a fixture folder. Passwords are synthetic container values.
 */
@Tag("recovery-it")
@Testcontainers
class RecoveryMigrationIT {

	private static final Path INFRA = Path.of("..", "infra", "postgres").toAbsolutePath().normalize();

	private static final Path FIXTURES = Path.of("src", "test", "resources", "flyway-fixtures").toAbsolutePath()
		.normalize();

	private static final String MIGRATOR = "rwb_migrator";

	private static final String MIGRATOR_PASSWORD = "it-migrator";

	private static final String RECOVERY_SVC_PASSWORD = "it-recovery";

	private static final String TEMPORAL_SVC_PASSWORD = "it-temporal";

	private static final AtomicInteger DATABASES = new AtomicInteger();

	/** Flyway's own table, from the one constant the production configuration holds (SEC/ponytail 5). */
	private static final String HISTORY = "recovery." + RecoveryFlywayConfig.HISTORY_TABLE;

	@Container
	static final PostgreSQLContainer POSTGRES = container();

	@Container
	static final PostgreSQLContainer SECOND = container();

	static PostgreSQLContainer container() {
		return new PostgreSQLContainer("postgres:16.16-alpine").withEnv("RWB_MIGRATOR_PASSWORD", MIGRATOR_PASSWORD)
			.withEnv("RECOVERY_SVC_PASSWORD", RECOVERY_SVC_PASSWORD)
			.withEnv("TEMPORAL_SVC_PASSWORD", TEMPORAL_SVC_PASSWORD)
			.withEnv("RWB_ACE_TIER2_PROBE", "false")
			.withEnv("RWB_LOAD_REFERENCE_SCHEMA", "false")
			.withCopyFileToContainer(MountableFile.forHostPath(INFRA.resolve("init")), "/docker-entrypoint-initdb.d")
			.withCopyFileToContainer(MountableFile.forHostPath(INFRA.resolve("schema")), "/schema")
			.waitingFor(Wait.forLogMessage(".*database system is ready to accept connections.*\\s", 2)
				.withStartupTimeout(Duration.ofMinutes(4)));
	}

	@Test
	void appliesOnceAndARerunAppliesNothing() throws SQLException {
		String database = newDatabase(POSTGRES);

		runner(database, location("apply-once")).run(context -> assertThat(context).hasNotFailed());

		assertThat(count(database, "select count(*) from " + HISTORY + " "
				+ "where script = 'V0001__rwb_e1_044_add_queue.sql'"))
			.isEqualTo(1);
		assertThat(count(database, "select count(*) from " + HISTORY + ""))
			.isEqualTo(1);
		assertThat(count(database,
				"select count(*) from information_schema.tables where table_schema = 'recovery' and table_name = 'queue'"))
			.isEqualTo(1);

		runner(database, location("apply-once")).run(context -> assertThat(context).hasNotFailed());

		assertThat(count(database, "select count(*) from " + HISTORY + "")).isEqualTo(1);
	}

	@Test
	void theSameFixtureCreatesTheTimerInTwoDatabasesWithEqualChecksums() throws SQLException {
		String first = newDatabase(POSTGRES);
		String second = newDatabase(SECOND);

		runner(POSTGRES, first, location("create-timer")).run(context -> assertThat(context).hasNotFailed());
		runner(SECOND, second, location("create-timer")).run(context -> assertThat(context).hasNotFailed());

		assertThat(count(POSTGRES, first,
				"select count(*) from information_schema.tables where table_schema = 'recovery' and table_name = 'timer'"))
			.isEqualTo(1);
		assertThat(count(SECOND, second,
				"select count(*) from information_schema.tables where table_schema = 'recovery' and table_name = 'timer'"))
			.isEqualTo(1);
		assertThat(checksum(POSTGRES, first, "V0001__rwb_e1_044_create_timer.sql"))
			.isEqualTo(checksum(SECOND, second, "V0001__rwb_e1_044_create_timer.sql"));
	}

	@Test
	void aChangedAppliedFileFailsValidationAndNamesTheVersion(@TempDir Path temp) throws IOException, SQLException {
		String database = newDatabase(POSTGRES);
		Path folder = copyFixture("invalid-checksum", temp);
		runner(database, location(folder)).run(context -> assertThat(context).hasNotFailed());
		Files.writeString(folder.resolve("V0001__rwb_e1_044_add_queue.sql"), "\n-- edited after apply\n",
				StandardOpenOption.APPEND);

		ListAppender<ILoggingEvent> logs = attach();
		try {
			runner(database, location(folder)).run(context -> {
				assertThat(context).hasFailed();
				assertThat(causes(context.getStartupFailure())).anyMatch(FlywayException.class::isInstance);
			});
		}
		finally {
			detach(logs);
		}

		assertThat(messages(logs)).containsExactly("MSG-P3-016 schema=recovery object=1");
		assertThat(count(database, "select count(*) from " + HISTORY + "")).isEqualTo(1);
	}

	@Test
	void cleanIsRefusedAndAChangedDatabaseIsNotTouched() throws SQLException {
		String database = newDatabase(POSTGRES);
		int[] objects = new int[1];

		runner(database, location("apply-once")).run(context -> {
			assertThat(context).hasNotFailed();
			objects[0] = countUnchecked(database,
					"select count(*) from information_schema.tables where table_schema = 'recovery'");
			Flyway flyway = context.getBean(Flyway.class);
			assertThatThrownBy(flyway::clean).isInstanceOf(FlywayException.class)
				.hasMessageContaining("disabled")
				.hasMessageNotContaining("MSG-P3-016");
		});

		assertThat(count(database, "select count(*) from information_schema.tables where table_schema = 'recovery'"))
			.isEqualTo(objects[0]);
	}

	@Test
	void aPreviousTagStartsAgainstALaterDatabaseAndAppliesNothing(@TempDir Path temp) throws IOException, SQLException {
		String database = newDatabase(POSTGRES);
		runner(database, location("previous-tag")).run(context -> assertThat(context).hasNotFailed());
		assertThat(count(database, "select count(*) from " + HISTORY + "")).isEqualTo(2);

		Path folder = copyFixture("previous-tag", temp);
		Files.delete(folder.resolve("V0002__rwb_e1_044_later.sql"));

		runner(database, location(folder)).run(context -> assertThat(context).hasNotFailed());

		assertThat(count(database, "select count(*) from " + HISTORY + "")).isEqualTo(2);
	}

	@Test
	void aLowerPendingVersionFailsWithItsVersion() throws SQLException {
		String database = newDatabase(POSTGRES);
		runner(database, location("higher-applied")).run(context -> assertThat(context).hasNotFailed());

		ListAppender<ILoggingEvent> logs = attach();
		try {
			runner(database, location("lower-pending")).run(context -> {
				assertThat(context).hasFailed();
				assertThat(causes(context.getStartupFailure())).anyMatch(FlywayException.class::isInstance);
			});
		}
		finally {
			detach(logs);
		}

		assertThat(messages(logs)).containsExactly("MSG-P3-016 schema=recovery object=2");
	}

	@Test
	void aMigrationThatFailsPartWayRollsBackAndNamesItsVersion() throws SQLException {
		String database = newDatabase(POSTGRES);

		ListAppender<ILoggingEvent> logs = attach();
		try {
			runner(database, location("failed-migration")).run(context -> {
				assertThat(context).hasFailed();
				assertThat(causes(context.getStartupFailure())).anyMatch(FlywayException.class::isInstance);
			});
		}
		finally {
			detach(logs);
		}

		assertThat(messages(logs)).containsExactly("MSG-P3-016 schema=recovery object=2");
		assertThat(count(database,
				"select count(*) from information_schema.tables where table_schema = 'recovery' and table_name = 'broken_a'"))
			.isZero();
		assertThat(count(database, "select count(*) from " + HISTORY + " "
				+ "where script = 'V0002__rwb_e1_044_broken.sql'"))
			.isZero();
	}

	@Test
	void driftComparisonFindsExactlyTheHandMadeColumn() throws SQLException {
		String left = newDatabase(POSTGRES);
		String right = newDatabase(POSTGRES);
		runner(left, location("drift")).run(context -> assertThat(context).hasNotFailed());
		runner(right, location("drift")).run(context -> assertThat(context).hasNotFailed());
		execute(right, "ALTER TABLE recovery.queue ADD COLUMN note_x text");

		SchemaSnapshot leftSnapshot = readSnapshot(left);
		SchemaSnapshot rightSnapshot = readSnapshot(right);
		List<SchemaDifference> differences = SchemaComparator.compare(leftSnapshot, rightSnapshot);

		assertThat(differences).singleElement().satisfies(difference -> {
			assertThat(difference.objectPath()).isEqualTo("recovery.queue.note_x");
			assertThat(difference.format()).isEqualTo("MSG-P3-016 schema=recovery object=recovery.queue.note_x");
		});
	}

	@Test
	void driftComparisonSeesAColumnLengthChange() throws SQLException {
		String left = newDatabase(POSTGRES);
		String right = newDatabase(POSTGRES);
		runner(left, location("drift")).run(context -> assertThat(context).hasNotFailed());
		runner(right, location("drift")).run(context -> assertThat(context).hasNotFailed());
		execute(right, "ALTER TABLE recovery.queue ALTER COLUMN team_code TYPE varchar(50)");

		List<SchemaDifference> differences = SchemaComparator.compare(readSnapshot(left), readSnapshot(right));

		assertThat(differences).singleElement().satisfies(difference -> {
			assertThat(difference.objectPath()).isEqualTo("recovery.queue.team_code");
			assertThat(difference.kind()).isEqualTo(SchemaDifference.Kind.CHANGED);
		});
	}

	@Test
	void twoContextsMigratingAtOnceApplyTheVersionOnceAndBothStart() throws Exception {
		String database = newDatabase(POSTGRES);
		CountDownLatch start = new CountDownLatch(1);
		ExecutorService pool = Executors.newFixedThreadPool(2);
		try {
			Future<Throwable> first = pool.submit(() -> migrateAfter(start, database));
			Future<Throwable> second = pool.submit(() -> migrateAfter(start, database));
			start.countDown();
			assertThat(first.get(2, TimeUnit.MINUTES)).isNull();
			assertThat(second.get(2, TimeUnit.MINUTES)).isNull();
		}
		finally {
			pool.shutdownNow();
		}

		assertThat(count(database, "select count(*) from " + HISTORY + " "
				+ "where script = 'V0001__rwb_e1_044_add_queue.sql'"))
			.isEqualTo(1);
	}

	@Test
	void aNonEmptyRecoverySchemaWithoutHistoryBaselinesAtZeroAndAppliesTheFirstVersion() throws SQLException {
		String database = newDatabase(POSTGRES);
		execute(database, "CREATE TABLE recovery.seed_marker (id int)");

		runner(database, location("non-empty-baseline")).run(context -> assertThat(context).hasNotFailed());

		assertThat(count(database, "select count(*) from " + HISTORY + " "
				+ "where type = 'BASELINE'"))
			.isEqualTo(1);
		assertThat(count(database, "select count(*) from " + HISTORY + " "
				+ "where script = 'V0001__rwb_e1_044_add_queue.sql'"))
			.isEqualTo(1);
	}

	@Test
	void migratorRightsAreExactlyTheTwoDRun14RightsAndAnForeignKeyIntoPublicIsRefused() throws SQLException {
		String database = newDatabase(POSTGRES);

		assertThat(flag(database, "select has_schema_privilege('rwb_migrator', 'public', 'USAGE')")).isTrue();
		assertThat(flag(database, "select has_schema_privilege('rwb_migrator', 'public', 'CREATE')")).isFalse();
		assertThat(count(database, "select count(*) from pg_auth_members where member = 'rwb_migrator'::regrole"))
			.isEqualTo(1);
		assertThat(count(database,
				"select count(*) from pg_auth_members where member = 'rwb_migrator'::regrole "
						+ "and roleid = 'ace_view_owner'::regrole and inherit_option = false and set_option = true "
						+ "and admin_option = false"))
			.isEqualTo(1);
		assertThat(flag(database,
				"select rolsuper or rolcreaterole or rolcreatedb or rolbypassrls from pg_roles where rolname = 'rwb_migrator'"))
			.isFalse();
		assertThat(count(database,
				"select count(*) from pg_class c join pg_namespace n on n.oid = c.relnamespace "
						+ "where n.nspname = 'public' and c.relkind in ('r', 'p', 'v', 'm', 'f') "
						+ "and has_table_privilege('rwb_migrator', c.oid, "
						+ "'SELECT, INSERT, UPDATE, DELETE, TRUNCATE, REFERENCES, TRIGGER')"))
			.isZero();

		try (Connection connection = DriverManager.getConnection(jdbc(POSTGRES, database), MIGRATOR,
				MIGRATOR_PASSWORD)) {
			assertThatThrownBy(() -> {
				try (Statement statement = connection.createStatement();
						ResultSet rows = statement.executeQuery("select count(*) from public.account")) {
					rows.next();
				}
			}).isInstanceOf(SQLException.class).satisfies(failure -> {
				SQLException sqlFailure = (SQLException) failure;
				assertThat(sqlFailure.getSQLState()).isEqualTo("42501");
				assertThat(sqlFailure.getMessage()).contains("permission denied for table account");
			});
		}

		ListAppender<ILoggingEvent> logs = attach();
		try {
			runner(database, location("fk-probe")).run(context -> {
				assertThat(context).hasFailed();
				SQLException sqlFailure = causes(context.getStartupFailure()).stream()
					.filter(SQLException.class::isInstance)
					.map(SQLException.class::cast)
					.findFirst()
					.orElseThrow(() -> new AssertionError("no SQLException in the cause chain"));
				assertThat(sqlFailure.getSQLState()).isEqualTo("42501");
				assertThat(sqlFailure.getMessage()).contains("permission denied for table account");
			});
		}
		finally {
			detach(logs);
		}
		assertThat(count(database, "select count(*) from " + HISTORY + " "
				+ "where script = 'V0001__rwb_e1_044_fk_probe.sql'"))
			.isZero();
	}

	private static Throwable migrateAfter(CountDownLatch start, String database) throws InterruptedException {
		start.await(1, TimeUnit.MINUTES);
		Throwable[] failure = new Throwable[1];
		runner(database, location("apply-once")).run(context -> failure[0] = context.getStartupFailure());
		return failure[0];
	}

	private static ApplicationContextRunner runner(String database, String location) {
		return runner(POSTGRES, database, location);
	}

	private static ApplicationContextRunner runner(PostgreSQLContainer container, String database, String location) {
		return new ApplicationContextRunner()
			.withUserConfiguration(MigrationPropertiesConfig.class, RecoveryFlywayConfig.class, TestDataSource.class)
			.withPropertyValues("rwb.schema=recovery", "rwb.flyway.enabled=true",
					"rwb.flyway.url=" + jdbc(container, database), "rwb.flyway.user=" + MIGRATOR,
					"rwb.flyway.password=" + MIGRATOR_PASSWORD, "rwb.flyway.location=" + location);
	}

	@Configuration(proxyBeanMethods = false)
	static class TestDataSource {

		@Bean
		DataSource serviceDataSource() {
			return new DriverManagerDataSource(jdbc(POSTGRES, "postgres"), POSTGRES.getUsername(),
					POSTGRES.getPassword());
		}

		@Bean
		DataSourceProperties dataSourceProperties() {
			return new DataSourceProperties();
		}

	}

	private static String newDatabase(PostgreSQLContainer container) throws SQLException {
		String name = "it_e1_044_" + DATABASES.incrementAndGet();
		try (Connection connection = DriverManager.getConnection(jdbc(container, "postgres"), container.getUsername(),
				container.getPassword());
				Statement statement = connection.createStatement()) {
			statement.execute("CREATE DATABASE " + name + " TEMPLATE ace");
		}
		return name;
	}

	private static String jdbc(PostgreSQLContainer container, String database) {
		return "jdbc:postgresql://" + container.getHost() + ":" + container.getMappedPort(5432) + "/" + database;
	}

	private static String location(String folder) {
		return location(FIXTURES.resolve(folder));
	}

	private static String location(Path folder) {
		return "filesystem:" + folder.toAbsolutePath().toString().replace('\\', '/') + "/";
	}

	private static Path copyFixture(String folder, Path temp) throws IOException {
		Path target = Files.createDirectories(temp.resolve(folder));
		try (Stream<Path> files = Files.list(FIXTURES.resolve(folder))) {
			for (Path file : files.toList()) {
				Files.copy(file, target.resolve(file.getFileName()));
			}
		}
		return target;
	}

	private static int count(String database, String sql) throws SQLException {
		return count(POSTGRES, database, sql);
	}

	private static int count(PostgreSQLContainer container, String database, String sql) throws SQLException {
		try (Connection connection = DriverManager.getConnection(jdbc(container, database), container.getUsername(),
				container.getPassword());
				Statement statement = connection.createStatement();
				ResultSet rows = statement.executeQuery(sql)) {
			rows.next();
			return rows.getInt(1);
		}
	}

	private static int countUnchecked(String database, String sql) {
		try {
			return count(database, sql);
		}
		catch (SQLException ex) {
			throw new IllegalStateException(ex);
		}
	}

	private static boolean flag(String database, String sql) throws SQLException {
		try (Connection connection = connect(database);
				Statement statement = connection.createStatement();
				ResultSet rows = statement.executeQuery(sql)) {
			rows.next();
			return rows.getBoolean(1);
		}
	}

	private static void execute(String database, String sql) throws SQLException {
		try (Connection connection = connect(database); Statement statement = connection.createStatement()) {
			statement.execute(sql);
		}
	}

	private static Integer checksum(PostgreSQLContainer container, String database, String script) throws SQLException {
		try (Connection connection = DriverManager.getConnection(jdbc(container, database), container.getUsername(),
				container.getPassword());
				Statement statement = connection.createStatement();
				ResultSet rows = statement.executeQuery(
						"select checksum from " + HISTORY + " where script = '" + script + "'")) {
			rows.next();
			return rows.getInt(1);
		}
	}

	private static SchemaSnapshot readSnapshot(String database) throws SQLException {
		try (Connection connection = connect(database)) {
			return SchemaSnapshotReader.read(connection, "recovery", RecoveryFlywayConfig.HISTORY_TABLE);
		}
	}

	private static Connection connect(String database) throws SQLException {
		return DriverManager.getConnection(jdbc(POSTGRES, database), POSTGRES.getUsername(), POSTGRES.getPassword());
	}

	private static List<Throwable> causes(Throwable failure) {
		List<Throwable> chain = new ArrayList<>();
		Throwable current = failure;
		while (current != null && !chain.contains(current)) {
			chain.add(current);
			current = current.getCause();
		}
		return chain;
	}

	private static ListAppender<ILoggingEvent> attach() {
		ListAppender<ILoggingEvent> appender = new ListAppender<>();
		appender.start();
		((Logger) LoggerFactory.getLogger(RecoveryMigrationRunner.class)).addAppender(appender);
		return appender;
	}

	private static void detach(ListAppender<ILoggingEvent> appender) {
		((Logger) LoggerFactory.getLogger(RecoveryMigrationRunner.class)).detachAppender(appender);
		appender.stop();
	}

	private static List<String> messages(ListAppender<ILoggingEvent> appender) {
		return appender.list.stream().map(ILoggingEvent::getFormattedMessage).toList();
	}

}
