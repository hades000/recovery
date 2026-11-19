package th.co.scb.ace.demo.recovery.access.internal;

import java.util.Map;

import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.http.HttpStatus;
import org.springframework.http.ProblemDetail;
import org.springframework.security.access.AccessDeniedException;
import org.springframework.web.bind.annotation.ExceptionHandler;
import org.springframework.web.bind.annotation.ResponseStatus;
import org.springframework.web.bind.annotation.RestControllerAdvice;
import org.springframework.web.servlet.resource.NoResourceFoundException;

import th.co.scb.ace.demo.recovery.access.api.ApiError;
import th.co.scb.ace.demo.recovery.access.api.ApiProblemException;
import th.co.scb.ace.demo.recovery.access.api.MessageResolver;

/**
 * Maps exceptions to {@code application/problem+json}. No exception text or stack trace reaches the
 * client; the message ID goes to the log (Error and Message Standard v4 A2).
 *
 * <p>SPEC-RWB-E1-042-025 and §10.2: the {@link ApiError} branch is unchanged. The
 * status-and-message-ID form ({@code error() == null}) renders through {@link ProblemFactory} and
 * logs one WARN line with the message ID (or {@code none}), the status, the trace ID and the cause's
 * class name plus the fixed text "cause suppressed". It never logs the cause's message, its stack
 * trace, the placeholders, the field value or the {@code detail} override (D-RUN-15, SPEC-027).
 */
@RestControllerAdvice(basePackages = "th.co.scb.ace.demo.recovery")
class ApiExceptionHandler {

	private static final Logger log = LoggerFactory.getLogger(ApiExceptionHandler.class);

	private final ProblemFactory problems;

	private final org.springframework.beans.factory.ObjectProvider<MessageResolver> messages;

	ApiExceptionHandler(ProblemFactory problems, org.springframework.beans.factory.ObjectProvider<MessageResolver> messages) {
		this.problems = problems;
		this.messages = messages;
	}

	@ExceptionHandler(ApiProblemException.class)
	ProblemDetail problem(ApiProblemException ex) {
		if (ex.error() != null) {
			log.warn("Recovery API problem {}", ex.error().messageCode(), ex.getCause());
			return problems.problem(ex.error(), ex.placeholders());
		}
		log.warn("Recovery API problem messageId={} status={} traceId={} cause={} cause suppressed",
				ex.messageId() == null ? "none" : ex.messageId(), ex.status().value(), problems.traceId(),
				ex.getCause() == null ? "none" : ex.getCause().getClass().getName());
		return problems.problem(ex, messages.getObject());
	}

	@ExceptionHandler(AccessDeniedException.class)
	ProblemDetail forbidden(AccessDeniedException ex) {
		return problems.problem(ApiError.NOT_PERMITTED, Map.of("action", "do this"));
	}

	@ExceptionHandler(NoResourceFoundException.class)
	ProblemDetail notFound(NoResourceFoundException ex) {
		return problems.problem(ApiError.NOT_IN_SCOPE, Map.of());
	}

	@ExceptionHandler(Exception.class)
	@ResponseStatus(HttpStatus.INTERNAL_SERVER_ERROR)
	ProblemDetail unexpected(Exception ex) {
		log.error("Unhandled recovery API error", ex);
		ProblemDetail p = ProblemDetail.forStatus(HttpStatus.INTERNAL_SERVER_ERROR);
		p.setTitle("Internal Server Error");
		return p;
	}
}
