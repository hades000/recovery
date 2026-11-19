package th.co.scb.ace.demo.recovery.casewf.config;

import static org.assertj.core.api.Assertions.assertThat;
import static org.mockito.ArgumentMatchers.any;
import static org.mockito.Mockito.mock;
import static org.mockito.Mockito.when;

import java.time.LocalDate;
import java.util.List;
import java.util.Map;

import ch.qos.logback.classic.Level;
import ch.qos.logback.classic.Logger;
import ch.qos.logback.classic.spi.ILoggingEvent;
import ch.qos.logback.core.read.ListAppender;
import org.junit.jupiter.api.AfterEach;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import org.slf4j.LoggerFactory;
import org.springframework.boot.health.contributor.Health;
import org.springframework.dao.DataAccessResourceFailureException;
import org.springframework.boot.health.contributor.Status;
import org.springframework.core.env.Environment;

import th.co.scb.ace.demo.recovery.casewf.config.api.BusinessDateProvider;
import th.co.scb.ace.demo.recovery.casewf.config.api.ParameterKey;
import th.co.scb.ace.demo.recovery.casewf.config.api.ParameterKeys;
import th.co.scb.ace.demo.recovery.casewf.config.api.ParameterNotInForceException;
import th.co.scb.ace.demo.recovery.casewf.config.api.ParameterValue;

/**
 * TC-E1-042-04 and TC-E1-042-32 (SPEC-RWB-E1-042-016): readiness is UP for an approved value in
 * force or for a default, DOWN with {@code MSG-P3-032} and {name, environment} for neither, and a
 * future-only approved row with a default never fails it.
 */
class ParameterStartupCheckTest {

	private static final LocalDate TODAY = LocalDate.of(2026, 12, 5);

	private static final ParameterKey<Integer> FIXTURE = new ParameterKey<>("fixture.required", Integer.class,
			"BUSINESS", "", "", "", null, "GLOBAL", true, "RW-COE", List.of("DEV", "SIT", "UAT", "PROD"),
			List.of("RWB-E1-042"), false, "TABLE", null, "A required fixture key with no default.");

	private static final ParameterKey<Integer> DEV_ONLY = new ParameterKey<>("fixture.devonly", Integer.class,
			"BUSINESS", "", "", "", null, "GLOBAL", true, "RW-COE", List.of("DEV"), List.of("RWB-E1-042"), false,
			"TABLE", null, "A required fixture key listed for DEV only.");

	private ParameterServiceImpl service;

	private Environment environment;

	private BusinessDateProvider businessDate;

	private final Logger logger = (Logger) LoggerFactory.getLogger(ParameterStartupCheck.class);

	private final ListAppender<ILoggingEvent> appender = new ListAppender<>();

	@BeforeEach
	void setUp() {
		service = mock(ParameterServiceImpl.class);
		environment = mock(Environment.class);
		businessDate = mock(BusinessDateProvider.class);
		when(businessDate.today()).thenReturn(TODAY);
		appender.start();
		logger.addAppender(appender);
	}

	@AfterEach
	void releaseLog() {
		logger.detachAppender(appender);
	}

	/** REVIEW-001 M6: a database outage is reported as such, not as every key missing. */
	@Test
	void aDatabaseOutageIsReportedAsUnavailable() {
		when(service.get(FIXTURE, TODAY)).thenThrow(new DataAccessResourceFailureException("synthetic outage"));

		Health health = check(FIXTURE, true, "PROD");

		assertThat(health.getStatus()).isEqualTo(Status.DOWN);
		assertThat(health.getDetails()).containsEntry("database", "unavailable")
			.doesNotContainKeys("messageCode", "missing");
	}

	/** REVIEW-001 M6: a readiness probe that sees the same state again logs nothing more. */
	@Test
	void theSameStateIsLoggedOnce() {
		when(service.get(FIXTURE, TODAY)).thenThrow(new ParameterNotInForceException("fixture.required"));
		ParameterStartupCheck check = new ParameterStartupCheck(source(FIXTURE), service, businessDate, environment,
				true, "PROD");

		check.health();
		check.health();
		check.health();

		assertThat(appender.list).filteredOn(event -> event.getLevel() == Level.WARN).hasSize(1);
	}

	@Test
	void upForAKeyWithAnApprovedValueInForce() {
		when(service.get(ParameterKeys.REFDATA_CACHE_TTL_SECONDS, TODAY))
			.thenReturn(new ParameterValue<>("refdata.cache.ttl-seconds", 300, 1, TODAY, "PROD"));

		Health health = check(ParameterKeys.REFDATA_CACHE_TTL_SECONDS, true, "PROD");

		assertThat(health.getStatus()).isEqualTo(Status.UP);
		assertThat(health.getDetails()).doesNotContainKey("messageCode");
	}

	@Test
	void upForADefault() {
		when(service.get(ParameterKeys.REFDATA_CACHE_TTL_SECONDS, TODAY))
			.thenReturn(new ParameterValue<>("refdata.cache.ttl-seconds", 300, 0, null, "PROD"));

		assertThat(check(ParameterKeys.REFDATA_CACHE_TTL_SECONDS, true, "PROD").getStatus()).isEqualTo(Status.UP);
	}

	@Test
	void downWhenNoValueInForceAndNoDefault() {
		when(service.get(FIXTURE, TODAY)).thenThrow(new ParameterNotInForceException("fixture.required"));

		Health health = check(FIXTURE, true, "PROD");

		assertThat(health.getStatus()).isEqualTo(Status.DOWN);
		assertThat(health.getDetails()).containsEntry("messageCode", "MSG-P3-032");
		assertThat((List<Map<String, String>>) health.getDetails().get("missing"))
			.containsExactly(Map.of("name", "fixture.required", "environment", "PROD"));
	}

	@Test
	void envMissingIsDown() {
		Health health = check(ParameterKeys.TEMPORAL_TARGET, true, "PROD");

		assertThat(health.getStatus()).isEqualTo(Status.DOWN);
		assertThat((List<Map<String, String>>) health.getDetails().get("missing"))
			.containsExactly(Map.of("name", "temporal.target", "environment", "PROD"));
	}

	@Test
	void envPresentIsUp() {
		when(environment.getProperty("rwb.temporal.target")).thenReturn("temporal:7233");

		assertThat(check(ParameterKeys.TEMPORAL_TARGET, true, "PROD").getStatus()).isEqualTo(Status.UP);
	}

	@Test
	void futureOnlyRowWithoutDefaultIsDownUntilItsDate() {
		when(service.get(FIXTURE, TODAY)).thenThrow(new ParameterNotInForceException("fixture.required"));

		assertThat(check(FIXTURE, true, "PROD").getStatus()).isEqualTo(Status.DOWN);
	}

	@Test
	void aFutureSeedNeverFailsReadiness() {
		when(service.get(ParameterKeys.CASE_ENTRY_DPD, TODAY))
			.thenReturn(new ParameterValue<>("case.entry.dpd", 90, 0, null, "PROD"));

		assertThat(check(ParameterKeys.CASE_ENTRY_DPD, true, "PROD").getStatus()).isEqualTo(Status.UP);
	}

	@Test
	void withTheFlagOffOnlyDefaultsAreChecked() {
		when(service.get(ParameterKeys.CASE_ENTRY_DPD, TODAY)).thenReturn(null);

		ParameterStartupCheck check = new ParameterStartupCheck(source(ParameterKeys.CASE_ENTRY_DPD), service,
				businessDate, environment, false, "PROD");

		assertThat(check.health().getStatus()).isEqualTo(Status.UP);
	}

	@Test
	void aKeyNotListedForTheRunningEnvironmentIsNotChecked() {
		ParameterStartupCheck check = new ParameterStartupCheck(source(DEV_ONLY), service, businessDate, environment,
				true, "SIT");

		assertThat(check.health().getStatus()).isEqualTo(Status.UP);
	}

	@SuppressWarnings("unchecked")
	private Health check(ParameterKey<?> key, boolean enabled, String runningEnvironment) {
		return new ParameterStartupCheck(source(key), service, businessDate, environment, enabled, runningEnvironment)
			.health();
	}

	private static CatalogSource source(ParameterKey<?> key) {
		return new CatalogSource() {
			@Override
			List<ParameterKey<?>> all() {
				return List.of(key);
			}
		};
	}

}
