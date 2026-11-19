package th.co.scb.ace.demo.recovery.casewf.config;

import static org.assertj.core.api.Assertions.assertThat;
import static org.assertj.core.api.Assertions.assertThatThrownBy;
import static org.springframework.security.test.web.servlet.request.SecurityMockMvcRequestPostProcessors.jwt;
import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.get;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.jsonPath;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.status;

import java.io.ByteArrayInputStream;
import java.nio.charset.StandardCharsets;
import java.nio.file.Path;
import java.time.Duration;
import java.time.LocalDate;
import java.util.List;
import java.util.Map;
import java.util.UUID;
import java.util.concurrent.CopyOnWriteArrayList;
import java.util.concurrent.atomic.AtomicReference;

import org.junit.jupiter.api.Tag;
import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.context.SpringBootTest;
import org.springframework.boot.test.context.TestConfiguration;
import org.springframework.boot.webmvc.test.autoconfigure.AutoConfigureMockMvc;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Import;
import org.springframework.context.annotation.Primary;
import org.springframework.jdbc.core.JdbcTemplate;
import org.springframework.test.context.DynamicPropertyRegistry;
import org.springframework.test.context.DynamicPropertySource;
import org.springframework.test.web.servlet.MockMvc;
import org.springframework.transaction.event.TransactionPhase;
import org.springframework.transaction.event.TransactionalEventListener;
import org.testcontainers.containers.wait.strategy.Wait;
import org.testcontainers.junit.jupiter.Container;
import org.testcontainers.junit.jupiter.Testcontainers;
import org.testcontainers.postgresql.PostgreSQLContainer;
import org.testcontainers.utility.MountableFile;

import th.co.scb.ace.demo.recovery.access.api.ApiProblemException;
import th.co.scb.ace.demo.recovery.casewf.config.api.BusinessDateProvider;
import th.co.scb.ace.demo.recovery.casewf.config.api.ParameterLoadHandler;
import th.co.scb.ace.demo.recovery.casewf.config.api.ParameterLoadResult;
import th.co.scb.ace.demo.recovery.casewf.config.api.ParameterKeys;
import th.co.scb.ace.demo.recovery.casewf.config.api.ParameterService;
import th.co.scb.ace.demo.recovery.casewf.config.api.ParameterVersionApproved;

/**
 * TC-E1-042-01, -04, -05, -06, -07, -08, -09, -10, -11, -16, -17, -18, -19, -20, -22, -23, -24, -28, -29, -31,
 * -32, -35, -36, -37, -38, -39 and -40: the System suite of the parameter catalog over the real
 * database and the real security chain. The three load operations are called through
 * {@link ParameterLoadHandler}, because RWB-E1-043 owns their HTTP path (D-RUN-10); the assertions are
 * the same depth an HTTP test would use. Every user ID is a synthetic UUID.
 */
@Tag("recovery-it")
@Testcontainers
@SpringBootTest(properties = { "rwb.p3.temporal=false", "rwb.p3.drools=false", "rwb.p3.configservice=true",
		"rwb.environment=PROD" })
@AutoConfigureMockMvc
@Import(ParameterConfigIT.TestBeans.class)
class ParameterConfigIT {

	private static final Path INFRA = Path.of("..", "infra", "postgres").toAbsolutePath().normalize();

	private static final UUID AUTHOR = UUID.fromString("00000000-0000-0000-0000-00000000b001");

	private static final UUID APPROVER = UUID.fromString("00000000-0000-0000-0000-00000000b002");

	private static final UUID CALLER = UUID.fromString("00000000-0000-0000-0000-00000000b003");

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
		registry.add("spring.datasource.url", ParameterConfigIT::aceUrl);
		registry.add("spring.datasource.username", () -> "recovery_svc");
		registry.add("spring.datasource.password", () -> "it-recovery");
		registry.add("rwb.flyway.url", ParameterConfigIT::aceUrl);
		registry.add("rwb.flyway.user", () -> "rwb_migrator");
		registry.add("rwb.flyway.password", () -> "it-migrator");
		registry.add("rwb.blob.connection-string", () -> "UseDevelopmentStorage=true");
	}

	@Autowired
	MockMvc mvc;

	@Autowired(required = false)
	ParameterLoadHandler handler;

	@Autowired
	ParameterService service;

	@Autowired
	JdbcTemplate jdbc;

	@Autowired
	TestBeans.Events events;

	@org.springframework.test.context.bean.override.mockito.MockitoSpyBean
	ParameterLoadValidator validatorSpy;

	@org.springframework.test.context.bean.override.mockito.MockitoSpyBean
	CatalogSource catalogSpy;

	@org.springframework.test.context.bean.override.mockito.MockitoSpyBean
	ParameterCache cacheSpy;

	@org.springframework.test.context.bean.override.mockito.MockitoSpyBean
	ParameterValueRepository valueRepository;

	@Autowired
	org.springframework.boot.health.actuate.endpoint.HealthEndpoint readiness;

	@Autowired
	ParameterStartupCheck parameterCatalog;

	@Autowired
	org.springframework.core.env.Environment environment;

	@Autowired
	TestBeans.MutableDate businessDate;

	@Autowired
	TestBeans.RecorderSwitch recorder;

	@Autowired
	TestBeans.ParameterLoadBranch branch;

	private static org.springframework.test.web.servlet.request.MockHttpServletRequestBuilder read(
			String... parameters) {
		var request = get("/api/recovery/v1/admin/parameters")
			.with(jwt().authorities(new org.springframework.security.core.authority.SimpleGrantedAuthority("RW-COE"))
				.jwt(token -> token.subject(AUTHOR.toString())
				.issuer("http://localhost:8090/entra")
				.audience(List.of("api://rwb-recovery"))
				.claim("roles", List.of("RW-COE"))));
		for (int index = 0; index < parameters.length; index += 2) {
			request = request.param(parameters[index], parameters[index + 1]);
		}
		return request;
	}

	@Test
	void prodContextReadsSeedVersionOne() throws Exception {
		mvc.perform(read("environment", "PROD").param("key", "caselist.export.maxrows"))
			.andExpect(status().isOk())
			.andExpect(jsonPath("$[0].key").value("caselist.export.maxrows"))
			.andExpect(jsonPath("$[0].valueInForce").value("10000"))
			.andExpect(jsonPath("$[0].versionNo").value(1))
			.andExpect(jsonPath("$[0].validFrom").value("2026-11-02"));
	}

	@Test
	void secretIsListedWithoutValue() throws Exception {
		mvc.perform(read("environment", "PROD").param("key", "ace.db.password"))
			.andExpect(status().isOk())
			.andExpect(jsonPath("$[0].key").value("ace.db.password"))
			.andExpect(jsonPath("$[0].owner").value("RW-PLATADM"))
			.andExpect(jsonPath("$[0].environments.length()").value(4))
			.andExpect(jsonPath("$[0].usedBy[0]").value("ACE common module"))
			.andExpect(jsonPath("$[0].valueInForce").doesNotExist())
			.andExpect(jsonPath("$[0].default").doesNotExist())
			.andExpect(jsonPath("$[0].versionNo").doesNotExist());
	}

	@Test
	void filtersByPrefixKindOwnerEnvironment() throws Exception {
		mvc.perform(read("environment", "PROD").param("key", "temporal.").param("kind", "ENVIRONMENT")
			.param("owner", "RW-PLATADM"))
			.andExpect(status().isOk())
			.andExpect(jsonPath("$.length()").value(4))
			.andExpect(jsonPath("$[0].kind").value("ENVIRONMENT"));
	}

	@Test
	void readWithoutTheRightIsRefused() throws Exception {
		mvc.perform(get("/api/recovery/v1/admin/parameters")
			.with(jwt().authorities(new org.springframework.security.core.authority.SimpleGrantedAuthority("RW-PHONECOL"))
				.jwt(token -> token.subject(CALLER.toString())
			.issuer("http://localhost:8090/entra")
			.audience(List.of("api://rwb-recovery"))
			.claim("roles", List.of("RW-PHONECOL")))))
			.andExpect(status().isForbidden())
			.andExpect(jsonPath("$.messageCode").value("MSG-P4-002"))
			.andExpect(jsonPath("$.detail").value("You cannot read parameters here. Your role does not include it."));
	}

	@Test
	void readinessIsUpOnTheSeededCatalog() {
		assertThat(parameterCatalog.health().getStatus()).isEqualTo(org.springframework.boot.health.contributor.Status.UP);
		assertThat(readiness.healthForPath("readiness").getStatus()).isEqualTo(org.springframework.boot.health.contributor.Status.UP);
		assertThat(environment.getProperty("management.endpoint.health.group.readiness.include"))
			.contains("parameterCatalog");
	}

	/** TC-32 / Ponytail Should 5: a required key with neither a value in force nor a default turns DOWN. */
	@Test
	void readinessIsDownNamingTheKeyAndEnvironmentWhenNoValueAndNoDefault() {
		jdbc.update("DELETE FROM parameter_value WHERE param_key = ? AND environment = ?", "refdata.cache.ttl-seconds",
				"PROD");
		// Deterministic: no earlier test's cached APPROVED list may satisfy the key (Ponytail New 11).
		cacheSpy.invalidateAll();
		java.util.List<th.co.scb.ace.demo.recovery.casewf.config.api.ParameterKey<?>> withoutDefault = ParameterKeys
			.all()
			.stream()
			.map(key -> key.name().equals("refdata.cache.ttl-seconds")
					? new th.co.scb.ace.demo.recovery.casewf.config.api.ParameterKey<>(key.name(), key.type(),
							key.kind(), key.unit(), key.min(), key.max(), null, key.scope(), key.required(),
							key.ownerRole(), key.environments(), key.usedBy(), key.secret(), key.valueSource(),
							key.envProperty(), key.description())
					: key)
			.toList();
		org.mockito.Mockito.doReturn(withoutDefault).when(catalogSpy).all();

		org.springframework.boot.health.contributor.Health health = parameterCatalog.health();

		assertThat(health.getStatus()).isEqualTo(org.springframework.boot.health.contributor.Status.DOWN);
		assertThat(readiness.healthForPath("readiness").getStatus()).isEqualTo(org.springframework.boot.health.contributor.Status.DOWN);
		assertThat(health.getDetails()).containsEntry("messageCode", "MSG-P3-032");
		assertThat((java.util.List<java.util.Map<String, String>>) health.getDetails().get("missing"))
			.containsExactly(java.util.Map.of("name", "refdata.cache.ttl-seconds", "environment", "PROD"));
	}

	/** TC-16 / Ponytail Must 1: after a rollback the same CSV can be loaded again. */
	@Test
	void aRolledBackLoadCanBeLoadedAgain() {
		LocalDate from = businessDate.today();
		ParameterLoadResult first = handler.load(csv("temporal.taskqueue.platform,DEV,synthetic-queue\n"), from,
				AUTHOR);
		handler.approve(first.loadId(), APPROVER);
		handler.rollback(first.loadId(), "synthetic rollback reason", CALLER);

		ParameterLoadResult reload = handler.load(csv("temporal.taskqueue.platform,DEV,synthetic-queue\n"), from,
				AUTHOR);

		assertThat(reload.repeat()).isFalse();
		assertThat(reload.loadId()).isNotEqualTo(first.loadId());
		assertThat(reload.status()).isEqualTo("VALIDATED");
		assertThat(handler.approve(reload.loadId(), APPROVER).status()).isEqualTo("APPROVED");
	}

	/** Ponytail Should 2: a value over the column width is a 422 refusal, never a 409. */
	@Test
	void aValueOverTheColumnWidthIsRefusedWhole() {
		assertThatThrownBy(() -> handler.load(csv("temporal.taskqueue.platform,UAT," + "q".repeat(401) + "\n"),
				businessDate.today(), AUTHOR))
			.isInstanceOf(ApiProblemException.class)
			.satisfies(ex -> {
				ApiProblemException problem = (ApiProblemException) ex;
				assertThat(problem.status().value()).isEqualTo(422);
				assertThat(problem.messageId()).isEqualTo("MSG-P1-002");
			});
	}

	/** TC-10 (b): a rollback whose commit fails leaves the rows APPROVED and the cache as it was. */
	@Test
	void failedRollbackCommitLeavesTheRowsApproved() throws Exception {
		LocalDate from = businessDate.today();
		ParameterLoadResult load = handler.load(csv("rules.testcases.min,DEV,57\n"), from, AUTHOR);
		handler.approve(load.loadId(), APPROVER);
		mvc.perform(read("environment", "DEV").param("key", "rules.testcases.min"))
			.andExpect(jsonPath("$[0].valueInForce").value("57"));

		TestBeans.BREAK_ROLLBACK.set(true);
		org.mockito.Mockito.clearInvocations(cacheSpy, valueRepository);
		try {
			assertThatThrownBy(() -> handler.rollback(load.loadId(), "synthetic rollback reason", CALLER))
				.isInstanceOf(RuntimeException.class);
		}
		finally {
			TestBeans.BREAK_ROLLBACK.set(false);
		}

		// Ponytail New 12: no rebuild was requested, so the value served next is the cached one.
		org.mockito.Mockito.verify(cacheSpy, org.mockito.Mockito.never()).invalidateAll();
		assertThat(rowStatus(load.loadId())).isEqualTo("APPROVED");
		assertThat(jdbc.queryForObject("SELECT rollback_reason FROM parameter_value WHERE load_id = ?", String.class,
				load.loadId())).isNull();
		mvc.perform(read("environment", "DEV").param("key", "rules.testcases.min"))
			.andExpect(jsonPath("$[0].valueInForce").value("57"));
	}

	/** SEC-042-04: a refused approval publishes nothing; a committed one publishes exactly once. */
	@Test
	void noEventOnARefusedApproval() {
		events.clear();
		ParameterLoadResult load = handler.load(csv("temporal.taskqueue.platform,SIT,synthetic-queue-2\n"),
				businessDate.today(), AUTHOR);

		assertThatThrownBy(() -> handler.approve(load.loadId(), AUTHOR)).isInstanceOf(ApiProblemException.class);

		assertThat(events.approved()).isEmpty();
	}

	@Test
	void eachEnvironmentResolvesItsOwnValue() throws Exception {
		LocalDate from = businessDate.today();
		ParameterLoadResult sit = handler.load(csv("case.entry.dpd,SIT,31\n"), from, AUTHOR);
		handler.approve(sit.loadId(), APPROVER);
		ParameterLoadResult prod = handler.load(csv("case.entry.dpd,PROD,301\n"), from, AUTHOR);
		handler.approve(prod.loadId(), APPROVER);

		mvc.perform(read("environment", "SIT").param("key", "case.entry.dpd"))
			.andExpect(jsonPath("$[0].valueInForce").value("31"));
		mvc.perform(read("environment", "PROD").param("key", "case.entry.dpd"))
			.andExpect(jsonPath("$[0].valueInForce").value("301"));
	}

	@Test
	void loadOutOfRangeIsRefusedWhole() {
		assertThatThrownBy(() -> handler.load(csv("case.entry.dpd,UAT,400\n"), businessDate.today(), AUTHOR))
			.isInstanceOf(ApiProblemException.class)
			.satisfies(ex -> assertThat(((ApiProblemException) ex).messageId()).isEqualTo("MSG-GEN-002"));
	}

	@Test
	void loadWrongTypeIsRefusedWhole() {
		assertThatThrownBy(() -> handler.load(csv("case.entry.dpd,UAT,ninety\n"), businessDate.today(), AUTHOR))
			.isInstanceOf(ApiProblemException.class)
			.satisfies(ex -> assertThat(((ApiProblemException) ex).messageId()).isEqualTo("MSG-P1-002"));
	}

	@Test
	void authorApproveIsRefused() {
		ParameterLoadResult load = handler.load(csv("caselist.export.maxrows,UAT,20000\n"), businessDate.today(),
				AUTHOR);

		assertThatThrownBy(() -> handler.approve(load.loadId(), AUTHOR))
			.isInstanceOf(ApiProblemException.class)
			.satisfies(ex -> assertThat(((ApiProblemException) ex).messageId()).isEqualTo("MSG-P7-002"));
	}

	@Test
	void identicalRepeatWritesNothing() {
		LocalDate from = businessDate.today();
		ParameterLoadResult first = handler.load(csv("caselist.export.maxrows,UAT,25000\n"), from, AUTHOR);
		ParameterLoadResult second = handler.load(csv("caselist.export.maxrows,UAT,25000\n"), from, AUTHOR);

		assertThat(second.loadId()).isEqualTo(first.loadId());
		assertThat(second.repeat()).isTrue();
	}

	/** CODE-001: an identical repeat of an APPROVED load returns it, not 409 MSG-P3-027. */
	@Test
	void anApprovedLoadRepeatsInsteadOfBeingRefused() {
		LocalDate from = businessDate.today();
		ParameterLoadResult first = handler.load(csv("temporal.taskqueue.platform,UAT,synthetic-queue-3\n"), from,
				AUTHOR);
		handler.approve(first.loadId(), APPROVER);

		ParameterLoadResult repeat = handler.load(csv("temporal.taskqueue.platform,UAT,synthetic-queue-3\n"), from,
				AUTHOR);

		assertThat(repeat.loadId()).isEqualTo(first.loadId());
		assertThat(repeat.repeat()).isTrue();
		assertThat(repeat.status()).isEqualTo("APPROVED");
		assertThat(jdbc.queryForObject("SELECT count(*) FROM parameter_value WHERE load_id = ?", Integer.class,
				first.loadId())).isEqualTo(1);
	}

	@Test
	void conflictingContentIsRefused() {
		LocalDate from = businessDate.today();
		ParameterLoadResult load = handler.load(csv("temporal.retention.days,UAT,45\n"), from, AUTHOR);
		handler.approve(load.loadId(), APPROVER);

		assertThatThrownBy(() -> handler.load(csv("temporal.retention.days,UAT,46\n"), from, AUTHOR))
			.isInstanceOf(ApiProblemException.class)
			.satisfies(ex -> {
				ApiProblemException problem = (ApiProblemException) ex;
				assertThat(problem.status().value()).isEqualTo(409);
				assertThat(problem.messageId()).isEqualTo("MSG-P3-027");
			});
	}

	@Test
	void blankRollbackReasonIsRefused() {
		ParameterLoadResult load = handler.load(csv("rules.testcases.min,UAT,55\n"), businessDate.today(), AUTHOR);
		handler.approve(load.loadId(), APPROVER);

		assertThatThrownBy(() -> handler.rollback(load.loadId(), "   ", CALLER))
			.isInstanceOf(ApiProblemException.class)
			.satisfies(ex -> {
				ApiProblemException problem = (ApiProblemException) ex;
				assertThat(problem.messageId()).isEqualTo("MSG-GEN-001");
				assertThat(problem.field()).isEqualTo("reason");
			});
	}

	@Test
	void rollbackReasonBoundary() {
		ParameterLoadResult load = handler.load(csv("rules.testcases.min,SIT,51\n"), businessDate.today(), AUTHOR);
		handler.approve(load.loadId(), APPROVER);

		assertThatThrownBy(() -> handler.rollback(load.loadId(), "x".repeat(401), CALLER))
			.isInstanceOf(ApiProblemException.class);
		assertThat(handler.rollback(load.loadId(), "x".repeat(400), CALLER).status()).isEqualTo("ROLLED_BACK");
	}

	@Test
	void rollbackWithNoEarlierVersionChangesNothing() {
		// A key whose only approved version comes from this load: the seeded rows are removed first.
		jdbc.update("DELETE FROM parameter_value WHERE param_key = ? AND environment = ?", "rules.testcases.min",
				"UAT");
		LocalDate from = businessDate.today();
		ParameterLoadResult load = handler.load(csv("rules.testcases.min,UAT,53\n"), from, AUTHOR);
		handler.approve(load.loadId(), APPROVER);

		assertThatThrownBy(() -> handler.rollback(load.loadId(), "synthetic reason", CALLER))
			.isInstanceOf(ApiProblemException.class)
			.satisfies(ex -> {
				ApiProblemException problem = (ApiProblemException) ex;
				assertThat(problem.messageId()).isEqualTo("MSG-P3-015");
				assertThat(problem.placeholders()).containsEntry("table", "PARAMETER");
			});
		assertThat(rowStatus(load.loadId())).isEqualTo("APPROVED");
		assertThat(jdbc.queryForObject("SELECT rollback_reason FROM parameter_value WHERE load_id = ?", String.class,
				load.loadId())).isNull();
	}

	@Test
	void onlyAnApprovedLoadCanBeRolledBack() {
		ParameterLoadResult load = handler.load(csv("caselist.export.maxrows,SIT,30000\n"), businessDate.today(),
				AUTHOR);

		assertThatThrownBy(() -> handler.rollback(load.loadId(), "synthetic reason", CALLER))
			.isInstanceOf(ApiProblemException.class)
			.satisfies(ex -> assertThat(((ApiProblemException) ex).messageId()).isEqualTo("MSG-P3-027"));
	}

	@Test
	void approveOfAnApprovedOrRolledBackLoadIsRefused() {
		ParameterLoadResult load = handler.load(csv("rules.testcases.min,PROD,52\n"), businessDate.today(), AUTHOR);
		handler.approve(load.loadId(), APPROVER);

		assertThatThrownBy(() -> handler.approve(load.loadId(), APPROVER))
			.isInstanceOf(ApiProblemException.class)
			.satisfies(ex -> assertThat(((ApiProblemException) ex).messageId()).isEqualTo("MSG-GEN-004"));
	}

	@Test
	void unknownLoadIdIs404ForApproveAndRollback() {
		UUID random = UUID.randomUUID();

		assertThatThrownBy(() -> handler.approve(random, APPROVER))
			.isInstanceOf(ApiProblemException.class)
			.satisfies(ex -> assertThat(((ApiProblemException) ex).error().messageCode()).isEqualTo("MSG-P4-003"));
		assertThatThrownBy(() -> handler.rollback(random, "synthetic reason", CALLER))
			.isInstanceOf(ApiProblemException.class)
			.satisfies(ex -> assertThat(((ApiProblemException) ex).error().messageCode()).isEqualTo("MSG-P4-003"));
		UUID seededRow = jdbc.queryForObject("SELECT id FROM parameter_value LIMIT 1", UUID.class);
		assertThatThrownBy(() -> handler.approve(seededRow, APPROVER)).isInstanceOf(ApiProblemException.class);
	}

	@Test
	void findHitsAndMissesAndAuditColumns() {
		LocalDate from = businessDate.today();
		ParameterLoadResult load = handler.load(csv("caselist.export.maxrows,PROD,40000\n"), from, AUTHOR);

		ParameterLoadResult found = handler.find(load.loadId()).orElseThrow();
		assertThat(found).isEqualTo(load);
		assertThat(handler.find(UUID.randomUUID())).isEmpty();

		Map<String, Object> row = jdbc.queryForMap("""
				SELECT created_by::text AS created_by, author_user_id::text AS author, is_active, state, created_at
				FROM parameter_value WHERE load_id = ?""", load.loadId());
		assertThat(row.get("created_by")).isEqualTo(AUTHOR.toString());
		assertThat(row.get("author")).isEqualTo(AUTHOR.toString());
		assertThat(row.get("is_active")).isEqualTo(true);
		assertThat(row.get("state")).isNull();
		assertThat(row.get("created_at")).isNotNull();
	}

	@Test
	void approvalPublishesOneEventWithNoUserId() {
		events.clear();
		ParameterLoadResult load = handler.load(csv("temporal.retention.days,PROD,31\n"), businessDate.today(),
				AUTHOR);

		handler.approve(load.loadId(), APPROVER);

		assertThat(events.approved()).hasSize(1);
		ParameterVersionApproved event = events.approved().get(0);
		assertThat(event.loadId()).isEqualTo(load.loadId());
		assertThat(event.paramKeys()).containsExactly("temporal.retention.days");
		assertThat(event.versions()).hasSize(1);
		assertThat(event.toString()).doesNotContain(AUTHOR.toString()).doesNotContain(APPROVER.toString());
	}

	@Test
	void recorderFailureLeavesRowsValidated() {
		ParameterLoadResult load = handler.load(csv("temporal.taskqueue.platform,PROD,other-queue\n"),
				businessDate.today(), AUTHOR);
		TestBeans.RECORDER_FAILS.set(true);
		try {
			assertThatThrownBy(() -> handler.approve(load.loadId(), APPROVER))
				.isInstanceOf(ApiProblemException.class)
				.satisfies(ex -> {
					ApiProblemException problem = (ApiProblemException) ex;
					assertThat(problem.messageId()).isEqualTo("MSG-P7-003");
					assertThat(problem.status().value()).isEqualTo(503);
				});
		}
		finally {
			TestBeans.RECORDER_FAILS.set(false);
		}

		assertThat(rowStatus(load.loadId())).isEqualTo("VALIDATED");
		assertThat(jdbc.queryForObject("SELECT count(*) FROM parameter_value WHERE load_id = ? AND approver_user_id IS NOT NULL",
				Integer.class, load.loadId())).isZero();
	}

	@Test
	void rollbackRestoresTheEarlierVersion() throws Exception {
		LocalDate from = businessDate.today();
		ParameterLoadResult load = handler.load(csv("case.entry.dpd,UAT,95\n"), from, AUTHOR);
		handler.approve(load.loadId(), APPROVER);
		int approvedBefore = events.approved().size();
		org.mockito.Mockito.clearInvocations(cacheSpy, valueRepository);
		assertThat(handler.rollback(load.loadId(), "synthetic rollback reason", CALLER).status())
			.isEqualTo("ROLLED_BACK");
		// SEC-042-04: a rollback publishes no ParameterVersionApproved.
		assertThat(events.approved()).hasSize(approvedBefore);
		// Ponytail New 12: the rollback asked for a rebuild, and the next read re-loads the versions
		// instead of answering from a stale cached list.
		org.mockito.Mockito.verify(cacheSpy, org.mockito.Mockito.times(1)).invalidateAll();
		mvc.perform(read("environment", "UAT").param("key", "case.entry.dpd"))
			.andExpect(jsonPath("$[0].valueInForce").value("90"));
		org.mockito.Mockito.verify(valueRepository, org.mockito.Mockito.atLeastOnce())
			.approved(org.mockito.ArgumentMatchers.anyString(), org.mockito.ArgumentMatchers.anyString());
		Map<String, Object> row = jdbc.queryForMap("""
				SELECT status, rollback_reason, updated_by::text AS updated_by, created_by::text AS created_by
				FROM parameter_value WHERE load_id = ?""", load.loadId());
		assertThat(row.get("status")).isEqualTo("ROLLED_BACK");
		assertThat(row.get("rollback_reason")).isEqualTo("synthetic rollback reason");
		assertThat(row.get("updated_by")).isEqualTo(CALLER.toString());
		assertThat(row.get("created_by")).isEqualTo(AUTHOR.toString());
	}

	@Test
	void approvalAfterTheBusinessDateMovedIsRefused() {
		LocalDate from = businessDate.today();
		ParameterLoadResult load = handler.load(csv("caselist.export.maxrows,UAT,41000\n"), from, AUTHOR);
		businessDate.today = from.plusDays(1);
		try {
			assertThatThrownBy(() -> handler.approve(load.loadId(), APPROVER))
				.isInstanceOf(ApiProblemException.class)
				.satisfies(ex -> assertThat(((ApiProblemException) ex).messageId()).isEqualTo("MSG-P3-027"));
		}
		finally {
			businessDate.today = from;
		}
		assertThat(rowStatus(load.loadId())).isEqualTo("VALIDATED");
	}

	@Test
	void futureVersionStartsOnItsDate() {
		LocalDate from = businessDate.today();
		ParameterLoadResult load = handler.load(csv("config.cache.ttl-seconds,PROD,61\n"), from.plusDays(5), AUTHOR);
		handler.approve(load.loadId(), APPROVER);

		assertThat(service.get(ParameterKeys.CONFIG_CACHE_TTL_SECONDS, from.plusDays(4)).value()).isEqualTo(60);
		assertThat(service.get(ParameterKeys.CONFIG_CACHE_TTL_SECONDS, from.plusDays(5)).value()).isEqualTo(61);
	}

	@Test
	void twoConcurrentIdenticalLoadsGiveOneLoadAndOneRepeat() throws Exception {
		LocalDate from = businessDate.today();
		java.util.concurrent.CyclicBarrier barrier = new java.util.concurrent.CyclicBarrier(2);
		org.mockito.Mockito.doAnswer(invocation -> {
			barrier.await(20, java.util.concurrent.TimeUnit.SECONDS);
			return invocation.callRealMethod();
		}).when(validatorSpy).validate(org.mockito.ArgumentMatchers.any(), org.mockito.ArgumentMatchers.any(),
				org.mockito.ArgumentMatchers.any());
		AtomicReference<ParameterLoadResult> one = new AtomicReference<>();
		AtomicReference<ParameterLoadResult> two = new AtomicReference<>();
		AtomicReference<RuntimeException> failure = new AtomicReference<>();
		Thread first = new Thread(() -> {
			try {
				one.set(handler.load(csv("temporal.retention.days,SIT,77\n"), from, AUTHOR));
			}
			catch (RuntimeException ex) {
				failure.set(ex);
			}
		});
		Thread second = new Thread(() -> {
			try {
				two.set(handler.load(csv("temporal.retention.days,SIT,77\n"), from, AUTHOR));
			}
			catch (RuntimeException ex) {
				failure.set(ex);
			}
		});
		first.start();
		second.start();
		first.join();
		second.join();

		assertThat(failure.get()).isNull();
		assertThat(one.get().loadId()).isEqualTo(two.get().loadId());
		assertThat(one.get().repeat() || two.get().repeat()).isTrue();
	}

	/**
	 * TC-20 (SPEC-014): two concurrent approvals of one load give one APPROVED and one 409 MSG-GEN-004.
	 * The latch holds both approvals inside their own transactions until both are about to take their
	 * locks (REVIEW-001 H1: the first lock is now the (key, environment) advisory lock, taken after
	 * {@code keyEnvironmentLocksOf}), so the two transactions overlap; no sleep decides the order.
	 */
	@Test
	void concurrentApprovalsGiveOneApprovedAndOne409() throws Exception {
		ParameterLoadResult load = handler.load(csv("caselist.export.maxrows,DEV,15000\n"), businessDate.today(),
				AUTHOR);
		java.util.concurrent.CountDownLatch bothInside = new java.util.concurrent.CountDownLatch(2);
		// The spy's own default answer reaches the real repository (it delegates for the JPA proxy).
		org.mockito.stubbing.Answer<?> real = org.mockito.Mockito.mockingDetails(valueRepository)
			.getMockCreationSettings()
			.getDefaultAnswer();
		org.mockito.Mockito.doAnswer(invocation -> {
			bothInside.countDown();
			if (!bothInside.await(20, java.util.concurrent.TimeUnit.SECONDS)) {
				throw new IllegalStateException("the second approval never reached the lock");
			}
			return real.answer(invocation);
		}).when(valueRepository).keyEnvironmentLocksOf(load.loadId());
		List<Object> outcomes = new CopyOnWriteArrayList<>();
		Runnable approve = () -> {
			try {
				outcomes.add(handler.approve(load.loadId(), APPROVER));
			}
			catch (RuntimeException ex) {
				outcomes.add(ex);
			}
		};
		Thread first = new Thread(approve);
		Thread second = new Thread(approve);
		first.start();
		second.start();
		first.join();
		second.join();

		assertThat(outcomes).hasSize(2);
		assertThat(outcomes).as("outcomes %s", outcomes)
			.filteredOn(ParameterLoadResult.class::isInstance)
			.singleElement()
			.satisfies(result -> assertThat(((ParameterLoadResult) result).status()).isEqualTo("APPROVED"));
		assertThat(outcomes).filteredOn(ApiProblemException.class::isInstance)
			.singleElement()
			.satisfies(ex -> {
				ApiProblemException problem = (ApiProblemException) ex;
				assertThat(problem.status().value()).isEqualTo(409);
				assertThat(problem.messageId()).isEqualTo("MSG-GEN-004");
			});
		assertThat(rowStatus(load.loadId())).isEqualTo("APPROVED");
	}

	/**
	 * REVIEW-001 H1: two different loads of one (key, environment) approved at the same moment. The
	 * later-dated approval is held inside its transaction after its row lock while the earlier-dated
	 * one runs. The earlier one must see the later one's committed approval and be refused (an approved
	 * version from a later date exists), and the {@code valid_to} chain stays consistent.
	 */
	@Test
	void concurrentApprovalsOfTwoLoadsForOneKeyAreSerialised() throws Exception {
		LocalDate today = businessDate.today();
		ParameterLoadResult later = handler.load(csv("refdata.cache.ttl-seconds,SIT,302\n"), today.plusDays(6),
				AUTHOR);
		ParameterLoadResult earlier = handler.load(csv("refdata.cache.ttl-seconds,SIT,301\n"), today.plusDays(5),
				AUTHOR);
		java.util.concurrent.CountDownLatch[] held = holdAfterRowLock(later.loadId());
		AtomicReference<Object> laterOutcome = new AtomicReference<>();
		AtomicReference<Object> earlierOutcome = new AtomicReference<>();

		Thread first = start(laterOutcome, () -> handler.approve(later.loadId(), APPROVER));
		assertThat(held[0].await(20, java.util.concurrent.TimeUnit.SECONDS)).isTrue();
		Thread second = start(earlierOutcome, () -> handler.approve(earlier.loadId(), APPROVER));
		awaitFinishedOrBlocked(second);
		held[1].countDown();
		first.join();
		second.join();

		assertThat(laterOutcome.get()).as("later approval").isInstanceOf(ParameterLoadResult.class);
		assertThat(earlierOutcome.get()).as("earlier approval").isInstanceOf(ApiProblemException.class);
		ApiProblemException refused = (ApiProblemException) earlierOutcome.get();
		assertThat(refused.status().value()).isEqualTo(409);
		assertThat(refused.messageId()).isEqualTo("MSG-P3-027");
		assertThat(rowStatus(earlier.loadId())).isEqualTo("VALIDATED");
		assertValidityChain("refdata.cache.ttl-seconds", "SIT");
	}

	/**
	 * REVIEW-001 H1: a rollback and an approval of one (key, environment) at the same moment. The
	 * rollback is held inside its transaction after its row lock while the approval runs. Both succeed
	 * one after the other, and the {@code valid_to} chain is the one a serial run gives.
	 */
	@Test
	void rollbackRacingAnApprovalOfTheSameKeyIsSerialised() throws Exception {
		LocalDate today = businessDate.today();
		ParameterLoadResult current = handler.load(csv("refdata.cache.ttl-seconds,UAT,305\n"), today.plusDays(5),
				AUTHOR);
		handler.approve(current.loadId(), APPROVER);
		ParameterLoadResult next = handler.load(csv("refdata.cache.ttl-seconds,UAT,306\n"), today.plusDays(6), AUTHOR);
		java.util.concurrent.CountDownLatch[] held = holdAfterRowLock(current.loadId());
		AtomicReference<Object> rollbackOutcome = new AtomicReference<>();
		AtomicReference<Object> approveOutcome = new AtomicReference<>();

		Thread rollback = start(rollbackOutcome,
				() -> handler.rollback(current.loadId(), "synthetic rollback reason", CALLER));
		assertThat(held[0].await(20, java.util.concurrent.TimeUnit.SECONDS)).isTrue();
		Thread approve = start(approveOutcome, () -> handler.approve(next.loadId(), APPROVER));
		awaitFinishedOrBlocked(approve);
		held[1].countDown();
		rollback.join();
		approve.join();

		assertThat(rollbackOutcome.get()).as("rollback").isInstanceOf(ParameterLoadResult.class);
		assertThat(approveOutcome.get()).as("approval").isInstanceOf(ParameterLoadResult.class);
		assertThat(rowStatus(current.loadId())).isEqualTo("ROLLED_BACK");
		assertThat(rowStatus(next.loadId())).isEqualTo("APPROVED");
		assertValidityChain("refdata.cache.ttl-seconds", "UAT");
	}

	/**
	 * REVIEW-001 CG-R001-02: the (key, environment) advisory locks are taken in ascending order of the
	 * value PostgreSQL locks (the 32-bit {@code hashtext}), not of the pair string, so every transaction
	 * takes them in one global order even when two pairs share a hash. The load has eight pairs, and the
	 * test first checks that their string order is not their lock-key order. The approval is refused
	 * after the locks (the business date moved past its valid from), so it changes nothing. The load
	 * starts 300 days ahead, after any version another test approves, so check 12 cannot refuse it.
	 */
	@Test
	void keyEnvironmentLocksAreTakenInAscendingLockKeyOrder() {
		LocalDate today = businessDate.today();
		LocalDate from = today.plusDays(300);
		StringBuilder rows = new StringBuilder();
		List<String> pairs = new java.util.ArrayList<>();
		for (String environment : List.of("DEV", "SIT", "UAT", "PROD")) {
			rows.append("refdata.cache.ttl-seconds,").append(environment).append(",311\n");
			rows.append("config.cache.ttl-seconds,").append(environment).append(",71\n");
			pairs.add("parameter_value|refdata.cache.ttl-seconds|" + environment);
			pairs.add("parameter_value|config.cache.ttl-seconds|" + environment);
		}
		List<Long> byString = pairs.stream().sorted().map(this::lockKey).toList();
		assertThat(byString).as("fixture: string order differs from lock-key order")
			.isNotEqualTo(byString.stream().sorted().toList());
		ParameterLoadResult load = handler.load(csv(rows.toString()), from, AUTHOR);
		org.mockito.Mockito.clearInvocations(valueRepository);
		businessDate.today = from.plusDays(1);
		try {
			assertThatThrownBy(() -> handler.approve(load.loadId(), APPROVER))
				.isInstanceOf(ApiProblemException.class)
				.satisfies(ex -> assertThat(((ApiProblemException) ex).messageId()).isEqualTo("MSG-P3-027"));
		}
		finally {
			businessDate.today = today;
		}

		List<Long> taken = org.mockito.Mockito.mockingDetails(valueRepository)
			.getInvocations()
			.stream()
			.filter(invocation -> invocation.getMethod().getName().equals("advisoryLock"))
			.map(invocation -> invocation.getArgument(0) instanceof String pair ? lockKey(pair)
					: ((Number) invocation.getArgument(0)).longValue())
			.toList();
		assertThat(taken).hasSize(pairs.size());
		assertThat(taken).as("lock keys in the order taken").isSorted();
		assertThat(jdbc.queryForList("SELECT DISTINCT status FROM parameter_value WHERE load_id = ?", String.class,
				load.loadId()))
			.containsExactly("VALIDATED");
	}

	/** The advisory-lock key PostgreSQL derives from a lock string. */
	private long lockKey(String text) {
		return jdbc.queryForObject("SELECT hashtext(?)::bigint", Long.class, text);
	}

	/** Holds the handler inside its transaction once {@code lockByLoadId(loadId)} returns: [inside, release]. */
	private java.util.concurrent.CountDownLatch[] holdAfterRowLock(UUID loadId) {
		java.util.concurrent.CountDownLatch inside = new java.util.concurrent.CountDownLatch(1);
		java.util.concurrent.CountDownLatch release = new java.util.concurrent.CountDownLatch(1);
		org.mockito.stubbing.Answer<?> real = org.mockito.Mockito.mockingDetails(valueRepository)
			.getMockCreationSettings()
			.getDefaultAnswer();
		org.mockito.Mockito.doAnswer(invocation -> {
			Object rows = real.answer(invocation);
			inside.countDown();
			if (!release.await(30, java.util.concurrent.TimeUnit.SECONDS)) {
				throw new IllegalStateException("the held transaction was never released");
			}
			return rows;
		}).when(valueRepository).lockByLoadId(loadId);
		return new java.util.concurrent.CountDownLatch[] { inside, release };
	}

	private static Thread start(AtomicReference<Object> outcome, java.util.function.Supplier<Object> action) {
		Thread thread = new Thread(() -> {
			try {
				outcome.set(action.get());
			}
			catch (RuntimeException ex) {
				outcome.set(ex);
			}
		});
		thread.start();
		return thread;
	}

	/**
	 * Waits until the thread has finished or a session of this database waits on a lock, so the held
	 * transaction is released only once the second operation has either run through or is blocked.
	 * The 50 ms join is a poll interval, not a guess at an order.
	 */
	private void awaitFinishedOrBlocked(Thread thread) throws InterruptedException {
		long deadline = System.nanoTime() + java.util.concurrent.TimeUnit.SECONDS.toNanos(20);
		while (thread.isAlive() && jdbc.queryForObject("""
				SELECT count(*) FROM pg_stat_activity
				WHERE datname = current_database() AND wait_event_type = 'Lock'""", Integer.class) == 0) {
			if (System.nanoTime() > deadline) {
				throw new IllegalStateException("the second operation neither finished nor waited on a lock");
			}
			thread.join(50);
		}
	}

	/** Each APPROVED version ends the day before the next one starts; the last one has no end. */
	private void assertValidityChain(String key, String environment) {
		List<LocalDate[]> versions = jdbc.query("""
				SELECT valid_from, valid_to FROM parameter_value
				WHERE param_key = ? AND environment = ? AND status = 'APPROVED' AND product_group IS NULL
				ORDER BY valid_from""",
				(rs, row) -> new LocalDate[] { rs.getObject(1, LocalDate.class), rs.getObject(2, LocalDate.class) },
				key, environment);
		assertThat(versions).isNotEmpty();
		for (int index = 0; index < versions.size(); index++) {
			LocalDate expected = index + 1 < versions.size() ? versions.get(index + 1)[0].minusDays(1) : null;
			assertThat(versions.get(index)[1]).as("valid_to of the version from %s", versions.get(index)[0])
				.isEqualTo(expected);
		}
	}

	/** TC-23 (SPEC-012, -023): unknown key, empty file and a past validFrom are refused and write nothing. */
	@Test
	void unknownKeyEmptyFileAndPastValidFrom() {
		LocalDate today = businessDate.today();
		Integer before = jdbc.queryForObject("SELECT count(*) FROM parameter_value", Integer.class);

		assertThatThrownBy(() -> handler.load(csv("not.a.key,PROD,1\n"), today, AUTHOR))
			.isInstanceOf(ApiProblemException.class)
			.satisfies(ex -> {
				ApiProblemException problem = (ApiProblemException) ex;
				assertThat(problem.status().value()).isEqualTo(422);
				assertThat(problem.messageId()).isEqualTo("MSG-P1-002");
			});
		assertThatThrownBy(() -> handler.load(new ByteArrayInputStream(new byte[0]), today, AUTHOR))
			.isInstanceOf(ApiProblemException.class)
			.satisfies(ex -> {
				ApiProblemException problem = (ApiProblemException) ex;
				assertThat(problem.status().value()).isEqualTo(422);
				assertThat(problem.messageId()).isEqualTo("MSG-GEN-001");
				assertThat(problem.field()).isEqualTo("file");
			});
		assertThatThrownBy(() -> handler.load(csv("case.entry.dpd,PROD,90\n"), today.minusDays(1), AUTHOR))
			.isInstanceOf(ApiProblemException.class)
			.satisfies(ex -> {
				ApiProblemException problem = (ApiProblemException) ex;
				assertThat(problem.status().value()).isEqualTo(422);
				assertThat(problem.messageId()).isEqualTo("MSG-P3-027");
				assertThat(problem.placeholders()).containsEntry("table", "PARAMETER");
			});
		assertThat(jdbc.queryForObject("SELECT count(*) FROM parameter_value", Integer.class)).isEqualTo(before);
	}

	/** TC-22 (SPEC-021), flag on: the stand-in for RWB-E1-043's PARAMETER branch delegates to the handler. */
	@Test
	void flagOnLoadsThroughTheAdapter() {
		ParameterLoadResult viaBranch = branch.load(csv("config.cache.ttl-seconds,DEV,62\n"), businessDate.today(),
				AUTHOR);

		assertThat(viaBranch.loadId()).isNotNull();
		assertThat(viaBranch.status()).isEqualTo("VALIDATED");
		assertThat(handler.find(viaBranch.loadId())).contains(viaBranch);
		assertThat(rowStatus(viaBranch.loadId())).isEqualTo("VALIDATED");
	}

	private String rowStatus(UUID loadId) {
		return jdbc.queryForObject("SELECT status FROM parameter_value WHERE load_id = ?", String.class, loadId);
	}

	private static java.io.InputStream csv(String text) {
		String file = "key,environment,value\n" + text;
		return new ByteArrayInputStream(file.getBytes(StandardCharsets.UTF_8));
	}


	@TestConfiguration
	static class TestBeans {

		@Bean
		@Primary
		MutableDate mutableDate() {
			return new MutableDate();
		}

		@Bean
		Events events() {
			return new Events();
		}

		@Bean
		@Primary
		RecorderSwitch recorderSwitch() {
			return new RecorderSwitch();
		}

		@Bean
		ParameterLoadBranch parameterLoadBranch(
				org.springframework.beans.factory.ObjectProvider<ParameterLoadHandler> handler) {
			return new ParameterLoadBranch(handler);
		}

		/**
		 * TC-22: a test-only stand-in for RWB-E1-043's PARAMETER branch (E43S SPEC-026). It takes the
		 * handler through ObjectProvider, as the SPEC-021 flag-off contract requires, and refuses with 404
		 * MSG-P4-003 when the handler is absent.
		 */
		static class ParameterLoadBranch {

			private final org.springframework.beans.factory.ObjectProvider<ParameterLoadHandler> handler;

			ParameterLoadBranch(org.springframework.beans.factory.ObjectProvider<ParameterLoadHandler> handler) {
				this.handler = handler;
			}

			ParameterLoadResult load(java.io.InputStream csv, LocalDate validFrom, UUID authorUserId) {
				ParameterLoadHandler available = handler.getIfAvailable();
				if (available == null) {
					throw new ApiProblemException(org.springframework.http.HttpStatus.NOT_FOUND, "MSG-P4-003", Map.of(),
							null, null, null);
				}
				return available.load(csv, validFrom, authorUserId);
			}
		}

		static final java.util.concurrent.atomic.AtomicBoolean RECORDER_FAILS = new java.util.concurrent.atomic.AtomicBoolean();

		static final java.util.concurrent.atomic.AtomicBoolean BREAK_ROLLBACK = new java.util.concurrent.atomic.AtomicBoolean();

		static class MutableDate implements BusinessDateProvider {

			private LocalDate today = LocalDate.of(2026, 12, 1);

			@Override
			public LocalDate today() {
				return today;
			}
		}

		static class Events {

			private final List<ParameterVersionApproved> received = new CopyOnWriteArrayList<>();

			@org.springframework.context.event.EventListener
			public void onApproved(ParameterVersionApproved event) {
				received.add(event);
			}

			List<ParameterVersionApproved> approved() {
				return List.copyOf(received);
			}

			void clear() {
				received.clear();
			}
		}

		/**
		 * Fails the decision recorder on demand, to prove the approval rolls back (TC-29 (b)). With
		 * BREAK_ROLLBACK set it makes the rollback's commit fail, before commit (TC-10 (b)); REVIEW-001 M4
		 * removed the rollback event this hook used to listen to, and M5 made rollback call the recorder.
		 */
		static class RecorderSwitch implements VersionDecisionRecorder {

			private volatile boolean fail;

			@Override
			@org.springframework.transaction.annotation.Transactional(propagation = org.springframework.transaction.annotation.Propagation.MANDATORY)
			public void recorded(String decisionCode, String outcome, String table, UUID loadId,
					List<String> keys, LocalDate validFrom, UUID approverUserId) {
				if (RECORDER_FAILS.get()) {
					throw new IllegalStateException("synthetic recorder marker");
				}
				if (BREAK_ROLLBACK.get()) {
					org.springframework.transaction.support.TransactionSynchronizationManager.registerSynchronization(
							new org.springframework.transaction.support.TransactionSynchronization() {
								@Override
								public void beforeCommit(boolean readOnly) {
									throw new IllegalStateException("synthetic commit failure");
								}
							});
				}
			}
		}
	}

	/**
	 * TC-22 (SPEC-021, AGENTS 3.13): with rwb.p3.configservice off the application starts, the load
	 * handler and the catalog endpoint are absent, the endpoint answers 404, and the catalog reader
	 * still serves a default without a database read.
	 */
	@org.junit.jupiter.api.Nested
	@SpringBootTest(properties = { "rwb.p3.temporal=false", "rwb.p3.drools=false", "rwb.p3.configservice=false",
			"rwb.environment=PROD" })
	@AutoConfigureMockMvc
	@Import(ParameterConfigIT.TestBeans.class)
	class FlagOff {

		@Autowired
		org.springframework.beans.factory.ObjectProvider<ParameterLoadHandler> handlerProvider;

		@Autowired
		th.co.scb.ace.demo.recovery.access.api.CatalogParameterReader reader;

		@Autowired
		MockMvc mvc;

		@Autowired
		TestBeans.ParameterLoadBranch branch;

		@Autowired
		JdbcTemplate jdbc;

		/** TC-22, flag off: the context starts and the branch stand-in refuses with 404 MSG-P4-003, writing nothing. */
		@Test
		void flagOffStillStartsAndRefusesParameterLoads() {
			assertThat(handlerProvider.getIfAvailable()).isNull();
			Integer before = jdbc.queryForObject("SELECT count(*) FROM parameter_value", Integer.class);

			assertThatThrownBy(() -> branch.load(csv("case.entry.dpd,DEV,91\n"), LocalDate.of(2026, 12, 1), AUTHOR))
				.isInstanceOf(ApiProblemException.class)
				.satisfies(ex -> {
					ApiProblemException problem = (ApiProblemException) ex;
					assertThat(problem.status().value()).isEqualTo(404);
					assertThat(problem.messageId()).isEqualTo("MSG-P4-003");
				});
			assertThat(jdbc.queryForObject("SELECT count(*) FROM parameter_value", Integer.class)).isEqualTo(before);
		}

		@Test
		void theHandlerAndTheEndpointAreAbsent() throws Exception {
			assertThat(handlerProvider.getIfAvailable()).isNull();
			mvc.perform(read("environment", "PROD")).andExpect(status().isNotFound());
		}

		@Test
		void theReaderStillServesTheDefault() {
			th.co.scb.ace.demo.recovery.access.api.CatalogParameterReader.Value<Integer> value = reader
				.get("case.entry.dpd", Integer.class);
			assertThat(value.value()).isEqualTo(90);
			assertThat(value.versionNo()).isZero();
		}

		@Test
		void theHandlerImplementsNoAccessApiType() {
			for (Class<?> type : ParameterLoadHandlerImpl.class.getInterfaces()) {
				assertThat(type.getPackageName()).as("implemented interface " + type.getName())
					.isNotEqualTo("th.co.scb.ace.demo.recovery.access.api");
			}
		}
	}
}
