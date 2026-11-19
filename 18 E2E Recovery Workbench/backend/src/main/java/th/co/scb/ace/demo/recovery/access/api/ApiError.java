package th.co.scb.ace.demo.recovery.access.api;

import java.util.Map;

/**
 * Messages the platform raises itself, with the English and Thai text of the Error and Message
 * Standard v4 section 4. The message table (reference data) is the source of record; story code
 * reads its messages from there. These few are held here only because the platform must answer
 * before any reference data is reachable (sign-in, permission, Temporal down).
 *
 * <p>Errors go out as {@code application/problem+json} with the API Specification v4
 * {@code Problem} fields: type, title, status, detail, messageCode, messageTh, field, traceId.
 */
public enum ApiError {

	/** E401: no valid session, or the person holds no Workbench role. */
	NO_ROLE("MSG-P4-001", 401,
			"You have no Recovery Workbench role. Ask your team manager to request one.",
			"คุณยังไม่มีสิทธิ์ใช้งาน Recovery Workbench กรุณาติดต่อผู้จัดการทีมเพื่อขอสิทธิ์"),

	/** E403: the role lacks the right in the capability area. Placeholder {action}. */
	NOT_PERMITTED("MSG-P4-002", 403,
			"You cannot {action} here. Your role does not include it.",
			"คุณไม่สามารถ{action}ได้ เนื่องจากบทบาทของคุณไม่มีสิทธิ์นี้"),

	/** E404: the record does not exist or is outside the caller's scope. */
	NOT_IN_SCOPE("MSG-P4-003", 404,
			"This case is not in your scope.",
			"กรณีนี้ไม่อยู่ในขอบเขตงานของคุณ"),

	/** E503: the Temporal frontend is unreachable (RWB-E1-071). */
	WORKFLOW_UNAVAILABLE("MSG-P3-036", 503,
			"The workflow service is not available. Try again in a few minutes.",
			"ระบบเวิร์กโฟลว์ไม่พร้อมใช้งาน กรุณาลองใหม่ในอีกไม่กี่นาที");

	private final String messageCode;
	private final int status;
	private final String english;
	private final String thai;

	ApiError(String messageCode, int status, String english, String thai) {
		this.messageCode = messageCode;
		this.status = status;
		this.english = english;
		this.thai = thai;
	}

	public String messageCode() {
		return messageCode;
	}

	public int status() {
		return status;
	}

	public String english(Map<String, String> placeholders) {
		return fill(english, placeholders);
	}

	public String thai(Map<String, String> placeholders) {
		return fill(thai, placeholders);
	}

	private static String fill(String text, Map<String, String> placeholders) {
		String out = text;
		for (Map.Entry<String, String> e : placeholders.entrySet()) {
			out = out.replace("{" + e.getKey() + "}", e.getValue());
		}
		return out;
	}
}
