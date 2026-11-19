package th.co.scb.ace.demo.e2e;

import static io.restassured.RestAssured.given;
import static org.hamcrest.Matchers.emptyOrNullString;
import static org.hamcrest.Matchers.equalTo;
import static org.hamcrest.Matchers.greaterThan;
import static org.hamcrest.Matchers.hasItem;
import static org.hamcrest.Matchers.matchesPattern;
import static org.hamcrest.Matchers.not;

import io.restassured.http.ContentType;
import org.junit.jupiter.api.Tag;
import org.junit.jupiter.api.Test;

/**
 * End-to-end checks against the running local stack: backend, Postgres, Temporal and the mock
 * Entra ID. Start the stack first ({@code scripts/dev.ps1 up -App}, or {@code up} plus bootRun),
 * then {@code ./gradlew e2eTest}. Tokens come from the mock OIDC server per role (infra/mock-oidc).
 * Expected responses follow API Specification v4.
 */
@Tag("e2e")
class PlatformE2ETest {

	private static final String API = System.getProperty("rwb.e2e.baseUrl", "http://localhost:8080") + "/api/recovery/v1";
	private static final String OIDC = System.getProperty("rwb.e2e.oidcUrl", "http://localhost:8090/entra");

	static String token(String clientId) {
		return given().contentType(ContentType.URLENC)
				.formParam("grant_type", "client_credentials")
				.formParam("client_id", clientId)
				.formParam("client_secret", "local")
				.formParam("scope", "api://rwb-recovery/.default")
				.post(OIDC + "/token")
				.then().statusCode(200)
				.extract().path("access_token");
	}

	@Test
	void noTokenIsRefusedWithMsgP4001() {
		given().get(API + "/platform/info")
				.then().statusCode(401)
				.contentType("application/problem+json")
				.body("messageCode", equalTo("MSG-P4-001"));
	}

	@Test
	void signedInPersonWithNoWorkbenchRoleIsRefusedWithMsgP4001() {
		given().auth().oauth2(token("rwb-local-norole"))
				.get(API + "/platform/info")
				.then().statusCode(401)
				.body("messageCode", equalTo("MSG-P4-001"))
				.body("messageTh", not(emptyOrNullString()));
	}

	@Test
	void platformInfoShowsTheAdr010Boundary() {
		given().auth().oauth2(token("rwb-local-audit"))
				.get(API + "/platform/info")
				.then().statusCode(200)
				.body("service", equalTo("ace-recovery"))
				.body("database.schema", equalTo("recovery"))
				.body("database.recoveryTables", greaterThan(90))
				.body("database.aceViews", equalTo(30))
				.body("database.visiblePublicTables", equalTo(0));
	}

	@Test
	void temporalHealthReportsNamespaceAndPlatformWorker() {
		given().auth().oauth2(token("rwb-local-platadm"))
				.get(API + "/admin/temporal/health")
				.then().statusCode(200)
				.body("namespace", equalTo("rwb-recovery"))
				.body("retentionDays", equalTo(30))
				.body("taskQueues.name", hasItem("rwb-platform"))
				.body("taskQueues.find { it.name == 'rwb-platform' }.workflowPollers", greaterThan(0));
	}

	/** postAdminWorkflowsSmoke: 202 with platform-smoke-{yyyymmdd}; a repeat returns the same ID. */
	@Test
	void platformSmokeWorkflowStarts() {
		String token = token("rwb-local-platadm");
		String id = given().auth().oauth2(token)
				.post(API + "/admin/workflows/smoke")
				.then().statusCode(202)
				.body("workflowId", matchesPattern("platform-smoke-\\d{8}"))
				.body("workflowType", equalTo("PlatformSmokeWorkflow"))
				.extract().path("workflowId");
		given().auth().oauth2(token)
				.post(API + "/admin/workflows/smoke")
				.then().statusCode(202)
				.body("workflowId", equalTo(id));
	}

	@Test
	void smokeNeedsPlatformAdminRight() {
		given().auth().oauth2(token("rwb-local-audit"))
				.post(API + "/admin/workflows/smoke")
				.then().statusCode(403)
				.contentType("application/problem+json")
				.body("messageCode", equalTo("MSG-P4-002"));
	}
}
