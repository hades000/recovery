package th.co.scb.ace.demo.recovery.access.api;

import java.util.Map;

/**
 * Resolves a message ID of the Error and Message Standard v4 in English and Thai
 * (SPEC-RWB-E1-042-022). Interim implementation: {@code access.internal.FixedMessageCatalog}.
 */
public interface MessageResolver {

	String english(String messageId, Map<String, String> placeholders);

	String thai(String messageId, Map<String, String> placeholders);
}