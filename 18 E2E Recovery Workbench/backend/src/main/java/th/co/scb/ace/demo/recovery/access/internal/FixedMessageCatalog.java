package th.co.scb.ace.demo.recovery.access.internal;

import java.util.Map;

import org.springframework.stereotype.Component;

import th.co.scb.ace.demo.recovery.access.api.MessageResolver;

/**
 * Interim message resolver over the nine IDs of SPEC-RWB-E1-042 10.3, copied from Error and Message
 * Standard v4 at the line the spec names. The message table that replaces it is OI-E1-042-004; the
 * Thai text is "Proposed" until DL10 approves it (S-08 line 19).
 */
@Component
class FixedMessageCatalog implements MessageResolver {

	private static final Map<String, Text> MESSAGES = Map.ofEntries(
			Map.entry("MSG-P3-032", new Text("Parameter {name} has no value for {environment}. The service did not start.",
					"พารามิเตอร์ {name} ยังไม่มีค่าสำหรับ {environment} ระบบจึงไม่เริ่มทำงาน")),
			Map.entry("MSG-GEN-002", new Text("{field} must be between {min} and {max}.",
					"{field} ต้องอยู่ระหว่าง {min} ถึง {max}")),
			Map.entry("MSG-P1-002", new Text("The {source} load for {date} was refused: {check}. The previous load is still in use.",
					"ระบบไม่รับข้อมูล {source} ของวันที่ {date} เนื่องจาก {check} ยังคงใช้ข้อมูลชุดก่อนหน้า")),
			Map.entry("MSG-GEN-001", new Text("Enter {field}.",
					"กรุณากรอก {field}")),
			Map.entry("MSG-P7-002", new Text("You prepared this decision, so you cannot approve it.",
					"คุณเป็นผู้จัดทำรายการนี้ จึงไม่สามารถอนุมัติได้")),
			Map.entry("MSG-P3-015", new Text("There is no earlier version of {table} to return to.",
					"ไม่มีฉบับก่อนหน้าของ {table} ให้ย้อนกลับ")),
			Map.entry("MSG-P3-027", new Text("The {table} load was refused: {check}. The version in force is unchanged.",
					"ระบบไม่รับข้อมูล {table} เนื่องจาก {check} ฉบับที่ใช้งานอยู่ยังไม่เปลี่ยนแปลง")),
			Map.entry("MSG-GEN-004", new Text("Someone else changed this record. Reload it to see their change.",
					"มีผู้อื่นแก้ไขรายการนี้แล้ว กรุณาโหลดใหม่เพื่อดูการเปลี่ยนแปลง")),
			Map.entry("MSG-P7-003", new Text("The action was not taken because the decision could not be recorded. Try again in a few minutes.",
					"ระบบยังไม่ดำเนินการ เนื่องจากบันทึกการตัดสินใจไม่สำเร็จ กรุณาลองใหม่อีกครั้งในอีกสักครู่"))
	);

	@Override
	public String english(String messageId, Map<String, String> placeholders) {
		return fill(text(messageId).english(), placeholders);
	}

	@Override
	public String thai(String messageId, Map<String, String> placeholders) {
		return fill(text(messageId).thai(), placeholders);
	}

	private static Text text(String messageId) {
		Text text = messageId == null ? null : MESSAGES.get(messageId);
		if (text == null) {
			throw new IllegalArgumentException("unknown message ID " + messageId);
		}
		return text;
	}

	private static String fill(String text, Map<String, String> placeholders) {
		String out = text;
		for (Map.Entry<String, String> entry : placeholders.entrySet()) {
			out = out.replace("{" + entry.getKey() + "}", entry.getValue());
		}
		return out;
	}

	/** One message in both languages. */
	record Text(String english, String thai) {
	}
}