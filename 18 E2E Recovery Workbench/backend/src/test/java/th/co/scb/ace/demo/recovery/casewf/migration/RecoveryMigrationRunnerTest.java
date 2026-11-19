package th.co.scb.ace.demo.recovery.casewf.migration;

import static com.tngtech.archunit.lang.syntax.ArchRuleDefinition.noClasses;
import static org.assertj.core.api.Assertions.assertThat;
import static org.assertj.core.api.Assertions.assertThatThrownBy;
import static org.mockito.Mockito.mock;
import static org.mockito.Mockito.when;

import java.util.List;

import javax.sql.DataSource;

import org.flywaydb.core.Flyway;
import org.flywaydb.core.api.ErrorDetails;
import org.flywaydb.core.api.FlywayException;
import org.flywaydb.core.api.MigrationInfo;
import org.flywaydb.core.api.MigrationInfoService;
import org.flywaydb.core.api.MigrationVersion;
import org.flywaydb.core.api.callback.Context;
import org.flywaydb.core.api.callback.Event;
import org.flywaydb.core.api.configuration.Configuration;
import org.flywaydb.core.api.exception.FlywayValidateException;
import org.flywaydb.core.api.output.ValidateOutput;
import org.flywaydb.core.api.output.ValidateResult;
import com.tngtech.archunit.core.importer.ClassFileImporter;
import com.tngtech.archunit.core.importer.ImportOption;
import org.junit.jupiter.api.AfterEach;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import org.slf4j.LoggerFactory;

import org.springframework.boot.jdbc.autoconfigure.DataSourceProperties;

import ch.qos.logback.classic.Level;
import ch.qos.logback.classic.Logger;
import ch.qos.logback.classic.spi.ILoggingEvent;
import ch.qos.logback.core.read.ListAppender;

/**
 * SPEC-RWB-E1-044-003, -001 (T-044-09, AC4, AC8): each failure kind logs exactly one
 * {@code MSG-P3-016 schema=recovery object=<…>} line and rethrows the same exception; the success
 * path logs nothing; both data-source branches of the factory are reachable.
 */
class RecoveryMigrationRunnerTest {

	private static final String SERVICE_URL = "jdbc:postgresql://localhost:5433/ace";

	private static final String MIGRATOR_URL = "jdbc:postgresql://migrator:5433/ace";

	private final ListAppender<ILoggingEvent> logs = new ListAppender<>();

	private Logger logger;

	@BeforeEach
	void attachLogCapture() {
		logger = (Logger) LoggerFactory.getLogger(RecoveryMigrationRunner.class);
		logs.start();
		logger.addAppender(logs);
	}

	@AfterEach
	void detachLogCapture() {
		logger.detachAppender(logs);
		logs.stop();
	}

	@Test
	void aValidationFailureNamesTheInvalidVersionAndRethrows() {
		Flyway flyway = mock(Flyway.class);
		FlywayValidateException failure = validateFailure();
		when(flyway.migrate()).thenThrow(failure);
		when(flyway.validateWithResult()).thenReturn(validateResult("7"));

		assertThatThrownBy(() -> runner(flyway).migrate()).isSameAs(failure);
		assertThat(logs.list).singleElement().satisfies(event -> {
			assertThat(event.getLevel()).isEqualTo(Level.ERROR);
			assertThat(event.getFormattedMessage()).isEqualTo("MSG-P3-016 schema=recovery object=7");
		});
	}

	@Test
	void aValidationFailureWithNoInvalidMigrationFallsThroughToThePendingVersion() {
		Flyway flyway = mock(Flyway.class);
		FlywayValidateException failure = validateFailure();
		when(flyway.migrate()).thenThrow(failure);
		when(flyway.validateWithResult()).thenReturn(validateResult());
		MigrationInfoService pending = pending("3");
		when(flyway.info()).thenReturn(pending);

		assertThatThrownBy(() -> runner(flyway).migrate()).isSameAs(failure);
		assertThat(logs.list).singleElement()
			.satisfies(event -> assertThat(event.getFormattedMessage()).isEqualTo("MSG-P3-016 schema=recovery object=3"));
	}

	/** CONF2-E044-04: the failed migration's version comes from the public error callback. */
	@Test
	void aMigrationThatFailsPartWayNamesTheVersionTheErrorCallbackRecorded() {
		Flyway flyway = mock(Flyway.class);
		FlywayException failure = new FlywayException("migration failed");
		when(flyway.migrate()).thenThrow(failure);
		RecoveryMigrationRunner.FailedVersion callback = new RecoveryMigrationRunner.FailedVersion();
		callback.handle(Event.AFTER_EACH_MIGRATE_ERROR, context("0002"));
		Configuration configuration = configuration(callback);
		when(flyway.getConfiguration()).thenReturn(configuration);
		MigrationInfoService pending = pending("3");
		when(flyway.info()).thenReturn(pending);

		assertThatThrownBy(() -> runner(flyway).migrate()).isSameAs(failure);
		assertThat(logs.list).singleElement()
			.satisfies(event -> assertThat(event.getFormattedMessage()).isEqualTo("MSG-P3-016 schema=recovery object=2"));
	}

	@Test
	void aConnectionFailureWithNoVersionUsesTheBeanName() {
		Flyway flyway = mock(Flyway.class);
		FlywayException failure = new FlywayException("connection refused");
		when(flyway.migrate()).thenThrow(failure);
		Configuration configuration = configuration(new RecoveryMigrationRunner.FailedVersion());
		when(flyway.getConfiguration()).thenReturn(configuration);
		MigrationInfoService pending = pending();
		when(flyway.info()).thenReturn(pending);

		assertThatThrownBy(() -> runner(flyway).migrate()).isSameAs(failure);
		assertThat(logs.list).singleElement().satisfies(event -> {
			assertThat(event.getFormattedMessage()).isEqualTo("MSG-P3-016 schema=recovery object=recoveryFlyway");
			assertThat(event.getFormattedMessage()).doesNotContain("jdbc").doesNotContain("password").doesNotContain("SELECT");
		});
	}

	/** CONF-E044-04: a failure with no version (lock timeout) reports the bean name, pending or not. */
	@Test
	void aFailureWithNoVersionUsesTheBeanNameEvenWhenVersionsArePending() {
		Flyway flyway = mock(Flyway.class);
		FlywayException failure = new FlywayException("lock timeout");
		when(flyway.migrate()).thenThrow(failure);
		Configuration configuration = configuration(new RecoveryMigrationRunner.FailedVersion());
		when(flyway.getConfiguration()).thenReturn(configuration);
		MigrationInfoService pending = pending("2", "3");
		when(flyway.info()).thenReturn(pending);

		assertThatThrownBy(() -> runner(flyway).migrate()).isSameAs(failure);
		assertThat(logs.list).singleElement()
			.satisfies(event -> assertThat(event.getFormattedMessage()).isEqualTo("MSG-P3-016 schema=recovery object=recoveryFlyway"));
	}

	@Test
	void aDetailLookupFailureStillLogsTheFallbackAndRethrowsTheOriginal() {
		Flyway flyway = mock(Flyway.class);
		FlywayException failure = new FlywayException("migration failed");
		when(flyway.migrate()).thenThrow(failure);
		when(flyway.getConfiguration()).thenThrow(new FlywayException("configuration also failed"));

		assertThatThrownBy(() -> runner(flyway).migrate()).isSameAs(failure);
		assertThat(logs.list).singleElement()
			.satisfies(event -> assertThat(event.getFormattedMessage()).isEqualTo("MSG-P3-016 schema=recovery object=recoveryFlyway"));
	}

	@Test
	void anInvalidVersionThatIsBlankFallsBackInsteadOfFailing() {
		Flyway flyway = mock(Flyway.class);
		FlywayValidateException failure = validateFailure();
		when(flyway.migrate()).thenThrow(failure);
		when(flyway.validateWithResult()).thenReturn(validateResult(""));
		MigrationInfoService pending = pending();
		when(flyway.info()).thenReturn(pending);

		assertThatThrownBy(() -> runner(flyway).migrate()).isSameAs(failure);
		assertThat(logs.list).singleElement()
			.satisfies(event -> assertThat(event.getFormattedMessage()).isEqualTo("MSG-P3-016 schema=recovery object=recoveryFlyway"));
	}

	@Test
	void aBrokenConnectionStillLogsTheFallbackAndRethrows() {
		RecoveryMigrationProperties properties = properties("jdbc:postgresql://127.0.0.1:1/ace", "rwb_migrator",
				"synthetic-password");
		Flyway flyway = new RecoveryFlywayConfig().recoveryFlyway(properties, mock(DataSource.class),
				dataSourceProperties());

		assertThatThrownBy(() -> new RecoveryMigrationRunner(flyway, properties).migrate())
			.isInstanceOf(FlywayException.class)
			.satisfies(failure -> assertThat(failure.getMessage().toLowerCase(java.util.Locale.ROOT)).contains("connect"));
		assertThat(logs.list).singleElement()
			.satisfies(event -> assertThat(event.getFormattedMessage()).isEqualTo("MSG-P3-016 schema=recovery object=recoveryFlyway"));
	}

	@Test
	void theFailedVersionCallbackListensOnlyToAMigrationErrorAndToleratesNoVersion() {
		RecoveryMigrationRunner.FailedVersion callback = new RecoveryMigrationRunner.FailedVersion();
		Context noInfo = mock(Context.class);
		Context noVersion = mock(Context.class);
		MigrationInfo info = mock(MigrationInfo.class);
		when(noVersion.getMigrationInfo()).thenReturn(info);

		assertThat(callback.supports(Event.AFTER_EACH_MIGRATE_ERROR, noInfo)).isTrue();
		assertThat(callback.supports(Event.AFTER_EACH_MIGRATE, noInfo)).isFalse();
		assertThat(callback.canHandleInTransaction(Event.AFTER_EACH_MIGRATE_ERROR, noInfo)).isTrue();
		assertThat(callback.getCallbackName()).isEqualTo("recoveryFailedVersion");
		callback.handle(Event.AFTER_EACH_MIGRATE_ERROR, context("0002"));
		callback.handle(Event.AFTER_EACH_MIGRATE_ERROR, noVersion);
		assertThat(RecoveryMigrationRunner.failureObject(flywayWith(callback), new FlywayException("x")))
			.isEqualTo("recoveryFlyway");
		callback.handle(Event.AFTER_EACH_MIGRATE_ERROR, context("0003"));
		callback.handle(Event.AFTER_EACH_MIGRATE_ERROR, noInfo);
		assertThat(RecoveryMigrationRunner.failureObject(flywayWith(callback), new FlywayException("x")))
			.isEqualTo("recoveryFlyway");
	}

	@Test
	void theSuccessPathLogsNoError() {
		Flyway flyway = mock(Flyway.class);

		runner(flyway).migrate();

		assertThat(logs.list).isEmpty();
	}

	@Test
	void bothDataSourceBranchesOfTheFactoryAreReachable() {
		DataSource serviceDataSource = mock(DataSource.class);
		RecoveryFlywayConfig config = new RecoveryFlywayConfig();

		Flyway withItsOwnUrl = config.recoveryFlyway(properties(MIGRATOR_URL, "rwb_migrator", ""), serviceDataSource,
				dataSourceProperties());
		Flyway onTheServiceDataSource = config.recoveryFlyway(properties("", "", ""), serviceDataSource,
				dataSourceProperties());

		assertThat(withItsOwnUrl.getConfiguration().getUrl()).isEqualTo(MIGRATOR_URL);
		assertThat(withItsOwnUrl.getConfiguration().getUser()).isEqualTo("rwb_migrator");
		assertThat(onTheServiceDataSource.getConfiguration().getDataSource()).isSameAs(serviceDataSource);
	}

	/**
	 * CONF2-E044-04: the migration code uses the public Flyway API only (SPEC-003, ASM-E044-12), so a
	 * Flyway upgrade cannot break it through an internal type.
	 */
	@Test
	void theMigrationCodeUsesOnlyThePublicFlywayApi() {
		noClasses().should()
			.dependOnClassesThat()
			.resideInAPackage("org.flywaydb.core.internal..")
			.check(new ClassFileImporter().withImportOption(ImportOption.Predefined.DO_NOT_INCLUDE_TESTS)
				.importPackagesOf(RecoveryMigrationRunner.class));
	}

	private static RecoveryMigrationRunner runner(Flyway flyway) {
		return new RecoveryMigrationRunner(flyway, properties(MIGRATOR_URL, "rwb_migrator", "synthetic-password"));
	}

	private static RecoveryMigrationProperties properties(String url, String user, String password) {
		return new RecoveryMigrationProperties("recovery",
				new RecoveryMigrationProperties.Flyway(true, url, user, password, "classpath:db/modulemigration/recovery"));
	}

	private static DataSourceProperties dataSourceProperties() {
		DataSourceProperties properties = new DataSourceProperties();
		properties.setUrl(SERVICE_URL);
		return properties;
	}

	private static Configuration configuration(RecoveryMigrationRunner.FailedVersion callback) {
		return Flyway.configure().callbacks(callback);
	}

	private static Flyway flywayWith(RecoveryMigrationRunner.FailedVersion callback) {
		Flyway flyway = mock(Flyway.class);
		Configuration configuration = configuration(callback);
		when(flyway.getConfiguration()).thenReturn(configuration);
		return flyway;
	}

	/** The callback context of a failed migration, as Flyway passes it with that migration's info. */
	private static Context context(String version) {
		Context context = mock(Context.class);
		MigrationInfo info = mock(MigrationInfo.class);
		when(info.getVersion()).thenReturn(MigrationVersion.fromVersion(version));
		when(context.getMigrationInfo()).thenReturn(info);
		return context;
	}

	private static FlywayValidateException validateFailure() {
		return new FlywayValidateException(new ErrorDetails(null, "Validate failed"), SERVICE_URL);
	}

	private static ValidateResult validateResult(String... versions) {
		List<ValidateOutput> invalidMigrations = java.util.Arrays.stream(versions)
			.map(version -> new ValidateOutput(version, "add queue", version.isBlank() ? "R__repeatable.sql"
					: "V%04d__rwb_e1_044_add_queue.sql".formatted(Integer.parseInt(version)),
					new ErrorDetails(null, "checksum mismatch")))
			.toList();
		return new ValidateResult("12.4.0", "PostgreSQL 16", new ErrorDetails(null, "Validate failed"), false,
				invalidMigrations.size(), invalidMigrations, List.of());
	}

	private static MigrationInfoService pending(String... versions) {
		MigrationInfoService service = mock(MigrationInfoService.class);
		MigrationInfo[] pending = java.util.Arrays.stream(versions).map(version -> {
			MigrationInfo info = mock(MigrationInfo.class);
			when(info.getVersion()).thenReturn(MigrationVersion.fromVersion(version));
			return info;
		}).toArray(MigrationInfo[]::new);
		when(service.pending()).thenReturn(pending);
		return service;
	}

}
