package th.co.scb.ace.demo.recovery.access.internal;

import java.io.IOException;
import java.net.URI;
import java.util.Map;

import io.micrometer.tracing.Tracer;
import jakarta.servlet.http.HttpServletResponse;
import org.springframework.beans.factory.ObjectProvider;
import org.springframework.http.HttpStatus;
import org.springframework.http.MediaType;
import org.springframework.http.ProblemDetail;
import org.springframework.stereotype.Component;
import tools.jackson.databind.json.JsonMapper;

import th.co.scb.ace.demo.recovery.access.api.ApiError;
import th.co.scb.ace.demo.recovery.access.api.ApiProblemException;
import th.co.scb.ace.demo.recovery.access.api.MessageResolver;

/** Builds API Specification v4 {@code Problem} bodies, in controllers and in the security filters. */
@Component
class ProblemFactory {

	private final ObjectProvider<Tracer> tracer;

	private final JsonMapper json;

	ProblemFactory(ObjectProvider<Tracer> tracer, JsonMapper json) {
		this.tracer = tracer;
		this.json = json;
	}

	ProblemDetail problem(ApiError error, Map<String, String> placeholders) {
		HttpStatus status = HttpStatus.valueOf(error.status());
		ProblemDetail p = ProblemDetail.forStatusAndDetail(status, error.english(placeholders));
		p.setType(URI.create("urn:rwb:problem:" + error.messageCode()));
		p.setTitle(status.getReasonPhrase());
		p.setProperty("messageCode", error.messageCode());
		p.setProperty("messageTh", error.thai(placeholders));
		p.setProperty("traceId", traceId());
		return p;
	}

	/**
	 * The status-and-message-ID form of SPEC-RWB-E1-042-022 and §10.2. With a message ID the body
	 * carries the resolver's EN and TH text, the field when set and the trace ID; the {@code detail}
	 * override replaces the EN text only. Without a message ID it is the status-only 503 of E7.
	 */
	ProblemDetail problem(ApiProblemException ex, MessageResolver messages) {
		HttpStatus status = ex.status();
		if (ex.messageId() == null) {
			ProblemDetail p = ProblemDetail.forStatus(status);
			p.setType(URI.create("urn:rwb:problem:unavailable"));
			p.setTitle(status.getReasonPhrase());
			p.setProperty("traceId", traceId());
			return p;
		}
		String detail = ex.detail() != null ? ex.detail() : messages.english(ex.messageId(), ex.placeholders());
		ProblemDetail p = ProblemDetail.forStatusAndDetail(status, detail);
		p.setType(URI.create("urn:rwb:problem:" + ex.messageId()));
		p.setTitle(status.getReasonPhrase());
		p.setProperty("messageCode", ex.messageId());
		p.setProperty("messageTh", messages.thai(ex.messageId(), ex.placeholders()));
		p.setProperty("traceId", traceId());
		if (ex.field() != null) {
			p.setProperty("field", ex.field());
		}
		return p;
	}

	void write(HttpServletResponse response, ApiError error, Map<String, String> placeholders) throws IOException {
		response.setStatus(error.status());
		response.setContentType(MediaType.APPLICATION_PROBLEM_JSON_VALUE);
		response.setCharacterEncoding("UTF-8");
		json.writeValue(response.getOutputStream(), problem(error, placeholders));
	}

	String traceId() {
		Tracer t = tracer.getIfAvailable();
		return t != null && t.currentSpan() != null ? t.currentSpan().context().traceId() : null;
	}
}
