package th.co.scb.ace.demo.recovery.access.api;

import java.util.Map;
import java.util.Objects;

import org.springframework.http.HttpStatus;

/**
 * Thrown by any recovery module to answer with a platform problem body. Two forms exist:
 * the platform {@link ApiError} form (unchanged) and, for this story, a status-and-message-ID form
 * carrying an Error and Message Standard v4 ID with its placeholders (SPEC-RWB-E1-042-022, -025).
 *
 * <p>For the message-ID form {@link #error()} is null; the message ID may be null only for the
 * status-only 503 of E7, and then no placeholders, field or detail are allowed. The exception's own
 * message is the message ID (or {@code "status-only 503"}), never user input.
 */
public class ApiProblemException extends RuntimeException {

	private final ApiError error;

	private final Map<String, String> placeholders;

	private final HttpStatus status;

	private final String messageId;

	private final String field;

	private final String detail;

	public ApiProblemException(ApiError error, Map<String, String> placeholders, Throwable cause) {
		super(error.messageCode(), cause);
		this.error = error;
		this.placeholders = Map.copyOf(placeholders);
		this.status = HttpStatus.valueOf(error.status());
		this.messageId = error.messageCode();
		this.field = null;
		this.detail = null;
	}

	public ApiProblemException(HttpStatus status, String messageId, Map<String, String> placeholders, String field,
			String detail, Throwable cause) {
		super(messageId != null ? messageId : "status-only 503", cause);
		Objects.requireNonNull(status, "status is required");
		Map<String, String> copy = placeholders == null ? Map.of() : Map.copyOf(placeholders);
		if (messageId == null) {
			if (status != HttpStatus.SERVICE_UNAVAILABLE) {
				throw new IllegalArgumentException("messageId is required unless the status is 503");
			}
			if (!copy.isEmpty() || field != null || detail != null) {
				throw new IllegalArgumentException(
						"the status-only 503 form takes no placeholders, field or detail");
			}
		}
		this.error = null;
		this.placeholders = copy;
		this.status = status;
		this.messageId = messageId;
		this.field = field;
		this.detail = detail;
	}

	/** Null for the status-and-message-ID form. */
	public ApiError error() {
		return error;
	}

	public Map<String, String> placeholders() {
		return placeholders;
	}

	public HttpStatus status() {
		return status;
	}

	public String messageId() {
		return messageId;
	}

	public String field() {
		return field;
	}

	public String detail() {
		return detail;
	}
}
