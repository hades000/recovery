package th.co.scb.ace.demo.recovery.access.internal;

import static org.assertj.core.api.Assertions.assertThat;
import static org.assertj.core.api.Assertions.assertThatThrownBy;
import static org.mockito.Mockito.mock;
import static org.mockito.Mockito.when;

import java.util.List;
import java.util.Map;

import ch.qos.logback.classic.Logger;
import ch.qos.logback.classic.spi.ILoggingEvent;
import ch.qos.logback.core.read.ListAppender;
import io.micrometer.tracing.Span;
import io.micrometer.tracing.TraceContext;
import io.micrometer.tracing.Tracer;
import org.junit.jupiter.api.AfterEach;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import org.slf4j.LoggerFactory;
import org.springframework.beans.factory.ObjectProvider;
import org.springframework.http.HttpMethod;
import org.springframework.http.HttpStatus;
import org.springframework.http.ProblemDetail;
import org.springframework.mock.web.MockHttpServletResponse;
import org.springframework.security.access.AccessDeniedException;
import org.springframework.web.servlet.resource.NoResourceFoundException;
import tools.jackson.databind.json.JsonMapper;

import th.co.scb.ace.demo.recovery.access.api.ApiError;
import th.co.scb.ace.demo.recovery.access.api.ApiProblemException;
import th.co.scb.ace.demo.recovery.access.api.MessageResolver;

/**
 * RWB-TE-001 SPEC-024 and RWB-E1-042 SPEC-022, -025, -027 (TC-E1-042-30): {@code ApiExceptionHandler}
 * maps exceptions to the API Specification v4 problem body, {@code ProblemFactory} fills the fields,
 * the trace ID and the response, and the new message-ID branch logs one safe WARN line.
 */
class ApiExceptionHandlerTest {

	private static final String MARKER = "synthetic-marker-7f3a";

	private final Logger logger = (Logger) LoggerFactory.getLogger(ApiExceptionHandler.class);

	private final ListAppender<ILoggingEvent> appender = new ListAppender<>();

	private final MessageResolver messages = new FixedMessageCatalog();

	@BeforeEach
	void captureLog() {
		appender.start();
		logger.addAppender(appender);
	}

	@AfterEach
	void releaseLog() {
		logger.detachAppender(appender);
	}

	@Test
	void apiProblemCarriesStatusTypeAndBothMessages() {
		ProblemDetail problem = handler(noTracer()).problem(
				new ApiProblemException(ApiError.NOT_PERMITTED, Map.of("action", "approve"), null));

		assertThat(problem.getStatus()).isEqualTo(403);
		assertThat(problem.getType().toString()).isEqualTo("urn:rwb:problem:MSG-P4-002");
		assertThat(problem.getProperties()).containsEntry("messageCode", "MSG-P4-002");
		assertThat(problem.getDetail()).isEqualTo("You cannot approve here. Your role does not include it.");
		assertThat((String) problem.getProperties().get("messageTh")).isEqualTo("คุณไม่สามารถapproveได้ เนื่องจากบทบาทของคุณไม่มีสิทธิ์นี้");
	}

	/** TC-30 (a): the existing branch renders as before and its own log line is unchanged. */
	@Test
	void apiErrorBranchUnchanged() {
		ProblemDetail problem = handler(noTracer()).problem(new ApiProblemException(ApiError.NOT_PERMITTED,
				Map.of("action", "read parameters"), new IllegalStateException(MARKER)));

		assertThat(problem.getStatus()).isEqualTo(403);
		assertThat(problem.getProperties()).containsEntry("messageCode", "MSG-P4-002");
		assertThat(problem.getDetail()).isEqualTo("You cannot read parameters here. Your role does not include it.");
		assertThat(appender.list).hasSize(1);
		assertThat(appender.list.get(0).getFormattedMessage()).contains("MSG-P4-002");
	}

	/** TC-30 (b): every field of the message-ID form is rendered. */
	@Test
	void messageIdFormRendersEveryField() {
		Tracer tracer = mock(Tracer.class);
		Span span = mock(Span.class);
		TraceContext context = mock(TraceContext.class);
		when(tracer.currentSpan()).thenReturn(span);
		when(span.context()).thenReturn(context);
		when(context.traceId()).thenReturn("trace-42");

		ProblemDetail problem = handler(provider(tracer)).problem(new ApiProblemException(HttpStatus.CONFLICT,
				"MSG-P3-027", Map.of("table", "PARAMETER", "check", "valid from is before the business date"), "validFrom",
				null, new IllegalStateException(MARKER)));

		assertThat(problem.getStatus()).isEqualTo(409);
		assertThat(problem.getType().toString()).isEqualTo("urn:rwb:problem:MSG-P3-027");
		assertThat(problem.getTitle()).isEqualTo("Conflict");
		assertThat(problem.getDetail()).isEqualTo(
				"The PARAMETER load was refused: valid from is before the business date. The version in force is unchanged.");
		assertThat(problem.getProperties()).containsEntry("messageCode", "MSG-P3-027")
			.containsEntry("field", "validFrom")
			.containsEntry("traceId", "trace-42");
		assertThat((String) problem.getProperties().get("messageTh")).contains("PARAMETER");
		assertOneSafeWarnLine("MSG-P3-027", "409");
	}

	/** TC-30 (c): the status-only 503 carries no message code and no detail. */
	@Test
	void statusOnly503HasNoMessageCode() {
		ProblemDetail problem = handler(noTracer()).problem(new ApiProblemException(HttpStatus.SERVICE_UNAVAILABLE,
				null, Map.of(), null, null, new IllegalStateException(MARKER)));

		assertThat(problem.getStatus()).isEqualTo(503);
		assertThat(problem.getType().toString()).isEqualTo("urn:rwb:problem:unavailable");
		assertThat(problem.getTitle()).isEqualTo("Service Unavailable");
		assertThat(problem.getDetail()).isNull();
		assertThat(problem.getProperties()).doesNotContainKey("messageCode").containsEntry("traceId", null);
		assertOneSafeWarnLine("none", "503");
	}

	/** TC-30 (d): a detail override replaces the EN text and never reaches the log. */
	@Test
	void detailOverrideReplacesTheEnglishText() {
		ProblemDetail problem = handler(noTracer()).problem(new ApiProblemException(HttpStatus.UNPROCESSABLE_ENTITY,
				"MSG-P1-002", Map.of("source", "PARAMETER", "date", "2026-12-01", "check", "row 2: x; row 5: y"),
				null, "row 2: x; row 5: y", new IllegalStateException(MARKER)));

		assertThat(problem.getDetail()).isEqualTo("row 2: x; row 5: y");
		assertThat(problem.getProperties()).containsEntry("messageCode", "MSG-P1-002");
		assertThat((String) problem.getProperties().get("messageTh")).isNotBlank();
		assertOneSafeWarnLine("MSG-P1-002", "422");
		assertThat(appender.list)
			.allSatisfy(event -> assertThat(event.getFormattedMessage()).doesNotContain("row 5"));
	}

	/** TC-30 (e): the constructor guards. */
	@Test
	void constructorGuards() {
		assertThatThrownBy(() -> new ApiProblemException(null, "MSG-GEN-004", Map.of(), null, null, null))
			.isInstanceOf(NullPointerException.class);
		assertThatThrownBy(() -> new ApiProblemException(HttpStatus.CONFLICT, null, Map.of(), null, null, null))
			.isInstanceOf(IllegalArgumentException.class);
		assertThatThrownBy(() -> new ApiProblemException(HttpStatus.SERVICE_UNAVAILABLE, null, Map.of("name", "x"),
				null, null, null))
			.isInstanceOf(IllegalArgumentException.class);
		assertThatThrownBy(() -> new ApiProblemException(HttpStatus.SERVICE_UNAVAILABLE, null, Map.of(), null,
				"detail", null))
			.isInstanceOf(IllegalArgumentException.class);
		assertThatThrownBy(() -> new ApiProblemException(HttpStatus.SERVICE_UNAVAILABLE, null, Map.of(), "field", null,
				null))
			.isInstanceOf(IllegalArgumentException.class);
	}

	@Test
	void accessDeniedIs403WithMsgP4002() {
		ProblemDetail problem = handler(noTracer()).forbidden(new AccessDeniedException("synthetic"));

		assertThat(problem.getStatus()).isEqualTo(403);
		assertThat(problem.getProperties()).containsEntry("messageCode", "MSG-P4-002");
	}

	@Test
	void missingResourceIs404WithMsgP4003() {
		ProblemDetail problem = handler(noTracer())
			.notFound(new NoResourceFoundException(HttpMethod.GET, "/api/recovery/v1/absent", "absent"));

		assertThat(problem.getStatus()).isEqualTo(404);
		assertThat(problem.getProperties()).containsEntry("messageCode", "MSG-P4-003");
	}

	@Test
	void otherExceptionIs500WithoutDetailOrMessageCode() {
		ProblemDetail problem = handler(noTracer()).unexpected(new IllegalStateException("synthetic detail"));

		assertThat(problem.getStatus()).isEqualTo(500);
		assertThat(problem.getTitle()).isEqualTo("Internal Server Error");
		assertThat(problem.getDetail()).isNull();
		assertThat(problem.getProperties()).isNull();
	}

	@Test
	void traceIdIsNullWithoutATracer() {
		assertThat(problem(noTracer()).getProperties()).containsEntry("traceId", null);
	}

	@Test
	void traceIdIsNullWhenNoSpanIsCurrent() {
		Tracer tracer = mock(Tracer.class);

		assertThat(problem(provider(tracer)).getProperties()).containsEntry("traceId", null);
	}

	@Test
	void traceIdComesFromTheCurrentSpan() {
		Tracer tracer = mock(Tracer.class);
		Span span = mock(Span.class);
		TraceContext context = mock(TraceContext.class);
		when(tracer.currentSpan()).thenReturn(span);
		when(span.context()).thenReturn(context);
		when(context.traceId()).thenReturn("trace-1");

		assertThat(problem(provider(tracer)).getProperties()).containsEntry("traceId", "trace-1");
	}

	@Test
	void writeSetsStatusContentTypeEncodingAndBody() throws Exception {
		MockHttpServletResponse response = new MockHttpServletResponse();

		new ProblemFactory(noTracer(), JsonMapper.builder().build()).write(response, ApiError.NOT_PERMITTED,
				Map.of("action", "approve"));

		assertThat(response.getStatus()).isEqualTo(HttpStatus.FORBIDDEN.value());
		assertThat(response.getContentType()).startsWith("application/problem+json");
		assertThat(response.getCharacterEncoding()).isEqualTo("UTF-8");
		assertThat(response.getContentAsString()).contains("MSG-P4-002").contains("messageTh");
	}

	private void assertOneSafeWarnLine(String messageId, String status) {
		List<ILoggingEvent> warns = appender.list.stream().filter(event -> event.getLevel().toString().equals("WARN"))
			.toList();
		assertThat(warns).hasSize(1);
		String line = warns.get(0).getFormattedMessage();
		assertThat(line).contains(messageId).contains(status).contains("cause suppressed")
			.contains("IllegalStateException");
		assertThat(line).doesNotContain(MARKER);
	}

	private ApiExceptionHandler handler(ObjectProvider<Tracer> tracer) {
		return new ApiExceptionHandler(new ProblemFactory(tracer, JsonMapper.builder().build()),
				messagesProvider());
	}

	private ObjectProvider<MessageResolver> messagesProvider() {
		ObjectProvider<MessageResolver> provider = mock(ObjectProvider.class);
		when(provider.getObject()).thenReturn(messages);
		return provider;
	}

	private static ProblemDetail problem(ObjectProvider<Tracer> tracer) {
		return new ProblemFactory(tracer, JsonMapper.builder().build()).problem(ApiError.NO_ROLE, Map.of());
	}

	@SuppressWarnings("unchecked")
	private static ObjectProvider<Tracer> noTracer() {
		ObjectProvider<Tracer> provider = mock(ObjectProvider.class);
		when(provider.getIfAvailable()).thenReturn(null);
		return provider;
	}

	@SuppressWarnings("unchecked")
	private static ObjectProvider<Tracer> provider(Tracer tracer) {
		ObjectProvider<Tracer> provider = mock(ObjectProvider.class);
		when(provider.getIfAvailable()).thenReturn(tracer);
		return provider;
	}
}
