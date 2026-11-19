package th.co.scb.ace.demo.recovery.casewf.config;

import static org.assertj.core.api.Assertions.assertThat;
import static org.assertj.core.api.Assertions.assertThatThrownBy;
import static org.hamcrest.Matchers.contains;
import static org.springframework.security.test.web.servlet.request.SecurityMockMvcRequestPostProcessors.jwt;
import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.get;
import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.post;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.content;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.jsonPath;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.status;

import java.io.ByteArrayInputStream;
import java.nio.charset.StandardCharsets;
import java.time.Duration;
import java.time.LocalDate;
import java.time.ZoneId;
import java.util.List;
import java.util.Map;
import java.util.UUID;
import java.util.concurrent.atomic.AtomicBoolean;

import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Nested;
import org.junit.jupiter.api.Tag;
import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.beans.factory.annotation.Qualifier;
import org.springframework.boot.test.context.SpringBootTest;
import org.springframework.boot.test.context.TestConfiguration;
import org.springframework.boot.webmvc.test.autoconfigure.AutoConfigureMockMvc;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Import;
import org.springframework.context.annotation.Primary;
import org.springframework.http.HttpStatus;
import org.springframework.http.MediaType;
import org.springframework.jdbc.core.JdbcTemplate;
import org.springframework.security.core.authority.SimpleGrantedAuthority;
import org.springframework.test.context.DynamicPropertyRegistry;
import org.springframework.test.context.DynamicPropertySource;
import org.springframework.test.web.servlet.MockMvc;
import org.springframework.test.web.servlet.request.MockHttpServletRequestBuilder;
import org.springframework.transaction.annotation.Propagation;
import org.springframework.transaction.annotation.Transactional;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.RestController;
import org.testcontainers.containers.wait.strategy.Wait;
import org.testcontainers.junit.jupiter.Container;
import org.testcontainers.junit.jupiter.Testcontainers;
import org.testcontainers.postgresql.PostgreSQLContainer;
import org.testcontainers.utility.MountableFile;

import th.co.scb.ace.demo.recovery.access.api.ApiError;
import th.co.scb.ace.demo.recovery.access.api.ApiProblemException;
import th.co.scb.ace.demo.recovery.casewf.config.api.ParameterLoadHandler;
import th.co.scb.ace.demo.recovery.casewf.config.api.ParameterLoadResult;

/**
 * API Tester suite for RWB-E1-042 (FTS-E1042-03, SPEC-RWB-E1-042-011, -020, -025; TC-09, TC-24,
 * TC-31, TC-34 and the interface cases of TC-05, TC-20, TC-29, TC-39).
 *
 * <p>HTTP cases drive the real controller, the real security filter chain, the method check and the
 * real {@code ApiExceptionHandler} over a Testcontainers PostgreSQL 16 built as the local stack.
 * The three reference-load operations have no controller in this story (D-RUN-10, D-RUN-20:
 * RWB-E1-043 owns the endpoint), so those cases call the published {@link ParameterLoadHandler} the
 * endpoint will render unchanged, and one flag-off case proves the documented PARAMETER-branch
 * refusal through a test-only stand-in for RWB-E1-043's branch. Every user ID is a synthetic UUID.
 */
@Tag("api")
@Testcontainers
@SpringBootTest(properties = { "rwb.p3.temporal=false", "rwb.p3.drools=false", "rwb.p3.configservice=true",
		"rwb.environment=PROD" })
@AutoConfigureMockMvc
@Import(ParameterApiContractIT.TestBeans.class)
class ParameterApiContractIT {

	private static final String PATH = "/api/recovery/v1/admin/parameters";

	private static final java.nio.file.Path INFRA = java.nio.file.Path.of("..", "infra", "postgres")
		.toAbsolutePath()
		.normalize();

	private static final UUID AUTHOR = UUID.fromString("00000000-0000-0000-0000-00000000a001");

	private static final UUID APPROVER = UUID.fromString("00000000-0000-0000-0000-00000000a002");

	private static final LocalDate FUTURE = LocalDate.now(ZoneId.of("Asia/Bangkok")).plusDays(10);

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
		registry.add("spring.datasource.url", ParameterApiContractIT::aceUrl);
		registry.add("spring.datasource.username", () -> "recovery_svc");
		registry.add("spring.datasource.password", () -> "it-recovery");
		registry.add("rwb.flyway.url", ParameterApiContractIT::aceUrl);
		registry.add("rwb.flyway.user", () -> "rwb_migrator");
		registry.add("rwb.flyway.password", () -> "it-migrator");
		registry.add("rwb.blob.connection-string", () -> "UseDevelopmentStorage=true");
	}

	@Autowired
	MockMvc mvc;

	@Autowired(required = false)
	ParameterLoadHandler handler;

	@Autowired
	JdbcTemplate jdbc;

	/**
	 * Spy on the catalog source in this class's own context (no extra Spring context, so no extra
	 * connection pool against the one Testcontainers database). It delegates to the real bean unless
	 * a test stubs it, and Spring resets it after each test.
	 */
	@org.springframework.test.context.bean.override.mockito.MockitoSpyBean
	CatalogSource catalogSpy;

	private static MockHttpServletRequestBuilder readAs(String role, String... parameters) {
		MockHttpServletRequestBuilder request = get(PATH).with(jwt()
			.authorities(new SimpleGrantedAuthority(role))
			.jwt(token -> token.subject(AUTHOR.toString())
				.issuer("http://localhost:8090/entra")
				.audience(List.of("api://rwb-recovery"))
				.claim("roles", List.of(role))));
		for (int index = 0; index < parameters.length; index += 2) {
			request = request.param(parameters[index], parameters[index + 1]);
		}
		return request;
	}

	private static java.io.InputStream csv(String rows) {
		return new ByteArrayInputStream(("key,environment,value\n" + rows).getBytes(StandardCharsets.UTF_8));
	}

	private int rowCount(String key, String environment) {
		Integer count = jdbc.queryForObject(
				"SELECT count(*) FROM parameter_value WHERE param_key = ? AND environment = ?", Integer.class, key,
				environment);
		return count == null ? 0 : count;
	}

	private String statusOf(UUID loadId) {
		return jdbc.queryForObject("SELECT status FROM parameter_value WHERE load_id = ?", String.class, loadId);
	}

	private UUID approvedLoad(String key, String environment, String value) {
		ParameterLoadResult loaded = handler.load(csv(key + "," + environment + "," + value), FUTURE, AUTHOR);
		return handler.approve(loaded.loadId(), APPROVER).loadId();
	}

	@Test
	@DisplayName("APT-GETPARAM-001 200 with the API v4 Parameter envelope for case.entry.dpd in PROD")
	void successEnvelope() throws Exception {
		mvc.perform(readAs("RW-COE", "environment", "PROD").param("key", "case.entry.dpd"))
			.andExpect(status().isOk())
			.andExpect(content().contentTypeCompatibleWith(MediaType.APPLICATION_JSON))
			.andExpect(jsonPath("$[0].key").value("case.entry.dpd"))
			.andExpect(jsonPath("$[0].kind").value("BUSINESS"))
			.andExpect(jsonPath("$[0].type").value("INTEGER"))
			.andExpect(jsonPath("$[0].unit").value("CALENDAR_DAYS"))
			.andExpect(jsonPath("$[0].min").value("1"))
			.andExpect(jsonPath("$[0].max").value("365"))
			.andExpect(jsonPath("$[0].default").value("90"))
			.andExpect(jsonPath("$[0].scope").value("GLOBAL"))
			.andExpect(jsonPath("$[0].required").value(true))
			.andExpect(jsonPath("$[0].owner").value("RW-COE"))
			.andExpect(jsonPath("$[0].environments", contains("DEV", "SIT", "UAT", "PROD")))
			.andExpect(jsonPath("$[0].usedBy", contains("recovery.casewf.casecreation")))
			.andExpect(jsonPath("$[0].secret").value(false))
			.andExpect(jsonPath("$[0].valueInForce").value("90"))
			.andExpect(jsonPath("$[0].versionNo").value(1))
			.andExpect(jsonPath("$[0].validFrom").value("2026-11-02"));
	}

	@Test
	@DisplayName("APT-GETPARAM-002 401 MSG-P4-001 for an unauthenticated call and for a token with no RW- role")
	void unauthenticatedIsRefused() throws Exception {
		mvc.perform(get(PATH)).andExpect(status().isUnauthorized())
			.andExpect(content().contentTypeCompatibleWith(MediaType.APPLICATION_PROBLEM_JSON))
			.andExpect(jsonPath("$.status").value(401))
			.andExpect(jsonPath("$.type").value("urn:rwb:problem:MSG-P4-001"))
			.andExpect(jsonPath("$.messageCode").value("MSG-P4-001"));

		mvc.perform(get(PATH).with(jwt().authorities(new SimpleGrantedAuthority("SCOPE_read"))))
			.andExpect(status().isUnauthorized())
			.andExpect(jsonPath("$.messageCode").value("MSG-P4-001"));
	}

	@Test
	@DisplayName("APT-GETPARAM-003 403 MSG-P4-002 with the action text for RW-PHONECOL")
	void forbiddenWithoutTheCapability() throws Exception {
		mvc.perform(readAs("RW-PHONECOL", "environment", "PROD"))
			.andExpect(status().isForbidden())
			.andExpect(content().contentTypeCompatibleWith(MediaType.APPLICATION_PROBLEM_JSON))
			.andExpect(jsonPath("$.status").value(403))
			.andExpect(jsonPath("$.type").value("urn:rwb:problem:MSG-P4-002"))
			.andExpect(jsonPath("$.messageCode").value("MSG-P4-002"))
			.andExpect(jsonPath("$.detail").value("You cannot read parameters here. Your role does not include it."));
	}

	@Test
	@DisplayName("APT-GETPARAM-004 422 MSG-GEN-002 field environment for an invalid environment")
	void unlistedEnvironmentIsRefused() throws Exception {
		mvc.perform(readAs("RW-COE", "environment", "FUTURE"))
			.andExpect(status().isUnprocessableEntity())
			.andExpect(content().contentTypeCompatibleWith(MediaType.APPLICATION_PROBLEM_JSON))
			.andExpect(jsonPath("$.status").value(422))
			.andExpect(jsonPath("$.messageCode").value("MSG-GEN-002"))
			.andExpect(jsonPath("$.field").value("environment"));
	}

	@Test
	@DisplayName("APT-GETPARAM-005 a secret row is listed with no value, default, version or validFrom")
	void secretRowHasNoValue() throws Exception {
		mvc.perform(readAs("RW-COE", "environment", "PROD").param("key", "ace.db.password"))
			.andExpect(status().isOk())
			.andExpect(jsonPath("$[0].key").value("ace.db.password"))
			.andExpect(jsonPath("$[0].secret").value(true))
			.andExpect(jsonPath("$[0].owner").value("RW-PLATADM"))
			.andExpect(jsonPath("$[0].usedBy", contains("ACE common module")))
			.andExpect(jsonPath("$[0].valueInForce").doesNotExist())
			.andExpect(jsonPath("$[0].default").doesNotExist())
			.andExpect(jsonPath("$[0].versionNo").doesNotExist())
			.andExpect(jsonPath("$[0].validFrom").doesNotExist());
	}

	/**
	 * E7 / SPEC-025: a database that cannot be reached during GET answers the status-only 503 Problem
	 * (API v4 lists 503 for getAdminParameters).
	 */
	@Test
	@DisplayName("APT-GETPARAM-006 503 status-only Problem when the database cannot be reached; no driver text leaks")
	void databaseFailureIsStatusOnly503() throws Exception {
		org.mockito.Mockito
			.doThrow(new org.springframework.dao.DataAccessResourceFailureException("synthetic driver text"))
			.when(catalogSpy)
			.all();

		mvc.perform(readAs("RW-COE", "environment", "PROD"))
			.andExpect(status().isServiceUnavailable())
			.andExpect(content().contentTypeCompatibleWith(MediaType.APPLICATION_PROBLEM_JSON))
			.andExpect(jsonPath("$.status").value(503))
			.andExpect(jsonPath("$.type").value("urn:rwb:problem:unavailable"))
			.andExpect(jsonPath("$.messageCode").doesNotExist())
			.andExpect(jsonPath("$.detail").doesNotExist())
			.andExpect(content().string(
					org.hamcrest.Matchers.not(org.hamcrest.Matchers.containsString("synthetic driver text"))));
	}

	@Test
	@DisplayName("APT-LOAD-001 422 MSG-P1-002 for a value over 400 characters, nothing written")
	void valueOverFourHundredCharactersIsRefused() {
		int before = rowCount("temporal.taskqueue.platform", "UAT");

		assertThatThrownBy(() -> handler.load(csv("temporal.taskqueue.platform,UAT," + "q".repeat(401)), FUTURE,
				AUTHOR))
			.isInstanceOfSatisfying(ApiProblemException.class, ex -> {
				assertThat(ex.status().value()).isEqualTo(422);
				assertThat(ex.messageId()).isEqualTo("MSG-P1-002");
				assertThat(ex.placeholders()).containsEntry("source", "PARAMETER");
				assertThat(ex.placeholders().get("check")).contains("longer than 400");
			});

		assertThat(rowCount("temporal.taskqueue.platform", "UAT")).isEqualTo(before);
	}

	private int rowsOfLoad(UUID loadId) {
		Integer count = jdbc.queryForObject("SELECT count(*) FROM parameter_value WHERE load_id = ?", Integer.class,
				loadId);
		return count == null ? 0 : count;
	}

	@Test
	@DisplayName("APT-LOAD-002 new load answers the ReferenceLoad fields with repeat=false; an identical repeat of the VALIDATED load returns it with repeat=true and writes nothing")
	void newLoadThenIdenticalRepeat() {
		int before = rowCount("caselist.export.maxrows", "UAT");

		ParameterLoadResult first = handler.load(csv("caselist.export.maxrows,UAT,25000"), FUTURE, AUTHOR);

		assertThat(first.loadId()).isNotNull();
		assertThat(first.table()).isEqualTo("PARAMETER");
		assertThat(first.validFrom()).isEqualTo(FUTURE);
		assertThat(first.status()).isEqualTo("VALIDATED");
		assertThat(first.rows()).isEqualTo(1);
		assertThat(first.repeat()).isFalse();
		assertThat(rowCount("caselist.export.maxrows", "UAT")).isEqualTo(before + 1);

		ParameterLoadResult repeat = handler.load(csv("caselist.export.maxrows,UAT,25000"), FUTURE, AUTHOR);

		assertThat(repeat.loadId()).isEqualTo(first.loadId());
		assertThat(repeat.repeat()).isTrue();
		assertThat(repeat.status()).isEqualTo("VALIDATED");
		assertThat(repeat.rows()).isEqualTo(1);
		assertThat(rowCount("caselist.export.maxrows", "UAT")).isEqualTo(before + 1);
	}

	@Test
	@DisplayName("APT-LOAD-003 an identical repeat of an APPROVED load returns it with repeat=true, not 409 (code-gate CODE-001)")
	void identicalRepeatOfAnApprovedLoad() {
		UUID loadId = approvedLoad("rules.testcases.min", "SIT", "70");
		int before = rowCount("rules.testcases.min", "SIT");

		ParameterLoadResult repeat = handler.load(csv("rules.testcases.min,SIT,70"), FUTURE, AUTHOR);

		assertThat(repeat.loadId()).isEqualTo(loadId);
		assertThat(repeat.repeat()).isTrue();
		assertThat(repeat.status()).isEqualTo("APPROVED");
		assertThat(repeat.table()).isEqualTo("PARAMETER");
		assertThat(repeat.validFrom()).isEqualTo(FUTURE);
		assertThat(repeat.rows()).isEqualTo(1);
		assertThat(rowsOfLoad(loadId)).isEqualTo(1);
		assertThat(rowCount("rules.testcases.min", "SIT")).isEqualTo(before);
		assertThat(statusOf(loadId)).isEqualTo("APPROVED");
	}

	@Test
	@DisplayName("APT-APPROVE-001 409 MSG-GEN-004 for a repeated approval of an approved load")
	void repeatedApprovalIsRefused() {
		UUID loadId = approvedLoad("rules.testcases.min", "DEV", "60");
		assertThat(statusOf(loadId)).isEqualTo("APPROVED");

		assertThatThrownBy(() -> handler.approve(loadId, APPROVER)).isInstanceOfSatisfying(ApiProblemException.class,
				ex -> {
					assertThat(ex.status().value()).isEqualTo(409);
					assertThat(ex.messageId()).isEqualTo("MSG-GEN-004");
					assertThat(ex.placeholders()).isEmpty();
				});
		assertThat(statusOf(loadId)).isEqualTo("APPROVED");
	}

	@Test
	@DisplayName("APT-APPROVE-002 409 MSG-P3-027 for conflicting content at an approved valid-from")
	void conflictingContentIsRefused() {
		approvedLoad("caselist.export.maxrows", "SIT", "20000");
		int before = rowCount("caselist.export.maxrows", "SIT");

		assertThatThrownBy(() -> handler.load(csv("caselist.export.maxrows,SIT,20001"), FUTURE, AUTHOR))
			.isInstanceOfSatisfying(ApiProblemException.class, ex -> {
				assertThat(ex.status().value()).isEqualTo(409);
				assertThat(ex.messageId()).isEqualTo("MSG-P3-027");
				assertThat(ex.placeholders()).containsEntry("table", "PARAMETER");
			});
		assertThat(rowCount("caselist.export.maxrows", "SIT")).isEqualTo(before);
	}

	@Test
	@DisplayName("APT-APPROVE-003 503 MSG-P7-003 when the decision recorder fails; rows stay VALIDATED")
	void recorderFailureIsServiceUnavailable() {
		ParameterLoadResult loaded = handler.load(csv("temporal.retention.days,UAT,45"), FUTURE, AUTHOR);
		TestBeans.RECORDER_FAILS.set(true);
		try {
			assertThatThrownBy(() -> handler.approve(loaded.loadId(), APPROVER))
				.isInstanceOfSatisfying(ApiProblemException.class, ex -> {
					assertThat(ex.status().value()).isEqualTo(503);
					assertThat(ex.messageId()).isEqualTo("MSG-P7-003");
					assertThat(ex.placeholders()).isEmpty();
					assertThat(ex.detail()).isNull();
					assertThat(ex.getCause()).hasMessage("synthetic recorder unavailable");
				});
			assertThat(statusOf(loaded.loadId())).isEqualTo("VALIDATED");
			assertThat(jdbc.queryForObject("SELECT approver_user_id FROM parameter_value WHERE load_id = ?",
					UUID.class, loaded.loadId()))
				.isNull();
		}
		finally {
			TestBeans.RECORDER_FAILS.set(false);
		}
	}

	@TestConfiguration
	static class TestBeans {

		static final AtomicBoolean RECORDER_FAILS = new AtomicBoolean();

		@Bean
		@Primary
		VersionDecisionRecorder failingRecorder() {
			return new FailingRecorder();
		}

		static class FailingRecorder implements VersionDecisionRecorder {

			@Override
			@Transactional(propagation = Propagation.MANDATORY)
			public void recorded(String decisionCode, String table, UUID loadId, List<String> keys,
					LocalDate validFrom, UUID approverUserId) {
				if (RECORDER_FAILS.get()) {
					throw new IllegalStateException("synthetic recorder unavailable");
				}
			}
		}
	}

	/**
	 * TC-22 (b) / SPEC-021: with the flag off the handler is absent and RWB-E1-043's PARAMETER branch
	 * refuses the operation with 404 MSG-P4-003. The branch stand-in below is a test double only; it
	 * is not a product endpoint and exists so the documented flag-off contract is asserted here.
	 */
	@Nested
	@SpringBootTest(properties = { "rwb.p3.temporal=false", "rwb.p3.drools=false", "rwb.p3.configservice=false",
			"rwb.environment=PROD" })
	@AutoConfigureMockMvc
	@Import({ ParameterApiContractIT.TestBeans.class, ParameterApiContractIT.ParameterLoadBranchStandIn.class })
	class FlagOff {

		@Autowired
		MockMvc mvc;

		@Autowired
		org.springframework.beans.factory.ObjectProvider<ParameterLoadHandler> handlers;

		@Test
		@DisplayName("APT-FLAGOFF-001 flag off: GET 404 and the PARAMETER branch refuses 404 MSG-P4-003")
		void flagOffRefusesTheParameterBranch() throws Exception {
			assertThat(handlers.getIfAvailable()).isNull();

			mvc.perform(readAs("RW-COE", "environment", "PROD")).andExpect(status().isNotFound());

			mvc.perform(post("/api/recovery/v1/admin/reference-loads")
				.with(jwt().authorities(new SimpleGrantedAuthority("RW-COE")))
				.param("table", "PARAMETER")
				.param("validFrom", FUTURE.toString()))
				.andExpect(status().isNotFound())
				.andExpect(content().contentTypeCompatibleWith(MediaType.APPLICATION_PROBLEM_JSON))
				.andExpect(jsonPath("$.status").value(404))
				.andExpect(jsonPath("$.messageCode").value("MSG-P4-003"));
		}
	}

	/** Test double for RWB-E1-043's PARAMETER branch; it never exists in product code. */
	@RestController
	static class ParameterLoadBranchStandIn {

		private final org.springframework.beans.factory.ObjectProvider<ParameterLoadHandler> handlers;

		ParameterLoadBranchStandIn(org.springframework.beans.factory.ObjectProvider<ParameterLoadHandler> handlers) {
			this.handlers = handlers;
		}

		@PostMapping("/api/recovery/v1/admin/reference-loads")
		org.springframework.http.ResponseEntity<String> load(@RequestParam String table,
				@RequestParam String validFrom) {
			ParameterLoadHandler handler = handlers.getIfAvailable();
			if (handler == null) {
				throw new ApiProblemException(ApiError.NOT_IN_SCOPE, Map.of(), null);
			}
			return org.springframework.http.ResponseEntity.status(HttpStatus.CREATED).body(table + ":" + validFrom);
		}
	}
}
