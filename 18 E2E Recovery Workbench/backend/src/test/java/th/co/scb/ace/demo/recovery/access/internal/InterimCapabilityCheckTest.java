package th.co.scb.ace.demo.recovery.access.internal;

import static org.assertj.core.api.Assertions.assertThat;
import static org.assertj.core.api.Assertions.assertThatThrownBy;

import java.util.List;
import java.util.Map;

import org.junit.jupiter.api.Test;
import org.springframework.core.io.FileSystemResource;
import org.springframework.security.authentication.TestingAuthenticationToken;
import org.springframework.security.core.Authentication;
import org.springframework.security.core.authority.SimpleGrantedAuthority;

import th.co.scb.ace.demo.recovery.access.api.ApiError;
import th.co.scb.ace.demo.recovery.access.api.ApiProblemException;

/**
 * TC-E1-042-24 (SPEC-RWB-E1-042-020; AUTH, X9): the interim capability seam grants exactly the
 * "Rules and parameters" rights of Users, Roles and Permissions v4, and {@code require} carries the
 * action text.
 */
class InterimCapabilityCheckTest {

	private static final String AREA = "Rules and parameters";

	private final InterimCapabilityCheck check = new InterimCapabilityCheck(
			new FileSystemResource("src/main/resources/access/interim-capability-grants.csv"));

	@Test
	void requireAndHas() {
		Authentication coe = token("RW-COE");

		assertThat(check.has(coe, AREA, "R")).isTrue();
		assertThat(check.require(coe, AREA, "R", "read parameters")).isTrue();
		assertThat(check.has(token("RW-RISK"), AREA, "A")).isTrue();
		assertThat(check.has(token("RW-REFADM"), AREA, "C")).isFalse();
		assertThat(check.has(token("RW-PHONECOL"), AREA, "R")).isFalse();
	}

	@Test
	void requireRefusalCarriesTheActionText() {
		assertThatThrownBy(() -> check.require(token("RW-PHONECOL"), AREA, "R", "read parameters"))
			.isInstanceOf(ApiProblemException.class)
			.satisfies(ex -> {
				ApiProblemException problem = (ApiProblemException) ex;
				assertThat(problem.error()).isEqualTo(ApiError.NOT_PERMITTED);
				assertThat(problem.placeholders()).containsEntry("action", "read parameters");
				assertThat(problem.placeholders()).doesNotContainValue("do this");
			});
	}

	@Test
	void hasNeverThrows() {
		assertThat(check.has(null, AREA, "R")).isFalse();
		assertThat(check.has(token("NOT-A-ROLE"), AREA, "R")).isFalse();
		assertThat(check.has(token("RW-COE"), "Unknown area", "R")).isFalse();
		assertThat(check.has(token("RW-COE"), AREA, "Z")).isFalse();
	}

	@Test
	void anUnknownRoleHasNoRights() {
		assertThat(check.has(token("PT-AGENCY"), AREA, "R")).isFalse();
	}

	@Test
	void aRoleAbsentFromTheFileIsRefused() {
		InterimCapabilityCheck narrow = new InterimCapabilityCheck(Map.of("RW-COE|Rules and parameters", "R"));

		assertThat(narrow.has(token("RW-RISK"), AREA, "R")).isFalse();
		assertThat(narrow.has(token("RW-COE"), AREA, "R")).isTrue();
	}

	@Test
	void theRolePrefixIsAccepted() {
		Authentication prefixed = new TestingAuthenticationToken("synthetic",
				"synthetic", List.of(new SimpleGrantedAuthority("ROLE_RW-COE")));

		assertThat(check.has(prefixed, AREA, "R")).isTrue();
	}

	@Test
	void theFileHoldsEveryRoleOfTheMatrix() {
		Map<String, String> grants = InterimCapabilityCheck
			.read(new FileSystemResource("src/main/resources/access/interim-capability-grants.csv"));

		assertThat(grants).hasSize(37);
		assertThat(grants.get("RW-COE|" + AREA)).isEqualTo("CRUD");
		assertThat(grants.get("RW-RISK|" + AREA)).isEqualTo("RA");
		assertThat(grants.get("RW-PHONECOL|" + AREA)).isEmpty();
	}

	private static Authentication token(String role) {
		return new TestingAuthenticationToken("synthetic", "synthetic", List.of(new SimpleGrantedAuthority(role)));
	}
}
