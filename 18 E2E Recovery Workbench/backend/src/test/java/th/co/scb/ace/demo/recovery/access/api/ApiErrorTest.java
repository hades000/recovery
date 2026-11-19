package th.co.scb.ace.demo.recovery.access.api;

import static org.assertj.core.api.Assertions.assertThat;

import java.util.Map;

import org.junit.jupiter.api.Test;

/**
 * RWB-TE-001 SPEC-024: {@code ApiError} and {@code ApiProblemException} keep their message code,
 * status, placeholder fill (English and Thai) and cause.
 */
class ApiErrorTest {

	@Test
	void everyConstantCarriesItsMessageCodeAndStatus() {
		assertThat(ApiError.NO_ROLE.messageCode()).isEqualTo("MSG-P4-001");
		assertThat(ApiError.NO_ROLE.status()).isEqualTo(401);
		assertThat(ApiError.NOT_PERMITTED.messageCode()).isEqualTo("MSG-P4-002");
		assertThat(ApiError.NOT_PERMITTED.status()).isEqualTo(403);
		assertThat(ApiError.NOT_IN_SCOPE.messageCode()).isEqualTo("MSG-P4-003");
		assertThat(ApiError.NOT_IN_SCOPE.status()).isEqualTo(404);
		assertThat(ApiError.WORKFLOW_UNAVAILABLE.messageCode()).isEqualTo("MSG-P3-036");
		assertThat(ApiError.WORKFLOW_UNAVAILABLE.status()).isEqualTo(503);
	}

	@Test
	void placeholdersAreFilledInEnglishAndThai() {
		assertThat(ApiError.NOT_PERMITTED.english(Map.of("action", "approve")))
			.isEqualTo("You cannot approve here. Your role does not include it.");
		assertThat(ApiError.NOT_PERMITTED.thai(Map.of("action", "approve"))).isEqualTo("คุณไม่สามารถapproveได้ เนื่องจากบทบาทของคุณไม่มีสิทธิ์นี้");
		assertThat(ApiError.NO_ROLE.english(Map.of())).startsWith("You have no Recovery Workbench role");
		assertThat(ApiError.NO_ROLE.english(Map.of("unused", "value"))).doesNotContain("{unused}");
	}

	@Test
	void exceptionCopiesPlaceholdersAndKeepsTheCauseAndMessageCode() {
		RuntimeException cause = new IllegalStateException("synthetic cause");

		ApiProblemException exception = new ApiProblemException(ApiError.NOT_PERMITTED,
				Map.of("action", "approve"), cause);

		assertThat(exception.getMessage()).isEqualTo("MSG-P4-002");
		assertThat(exception.error()).isEqualTo(ApiError.NOT_PERMITTED);
		assertThat(exception.placeholders()).containsEntry("action", "approve");
		assertThat(exception.getCause()).isSameAs(cause);
	}
}
