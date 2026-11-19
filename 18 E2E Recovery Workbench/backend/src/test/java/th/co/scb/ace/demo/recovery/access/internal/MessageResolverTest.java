package th.co.scb.ace.demo.recovery.access.internal;

import static org.assertj.core.api.Assertions.assertThat;
import static org.assertj.core.api.Assertions.assertThatThrownBy;

import java.util.List;
import java.util.Map;

import org.junit.jupiter.api.Test;

import th.co.scb.ace.demo.recovery.access.api.MessageResolver;

/**
 * TC-E1-042-30 (SPEC-RWB-E1-042-022): every ID of the message catalogue resolves in English and
 * Thai with the same placeholders, and an unknown ID fails loudly.
 */
class MessageResolverTest {

	private static final List<String> IDS = List.of("MSG-P3-032", "MSG-GEN-002", "MSG-P1-002", "MSG-GEN-001",
			"MSG-P7-002", "MSG-P3-015", "MSG-P3-027", "MSG-GEN-004", "MSG-P7-003");

	private final MessageResolver resolver = new FixedMessageCatalog();

	@Test
	void everyMessageResolvesInEnglishAndThai() {
		for (String id : IDS) {
			assertThat(resolver.english(id, Map.of())).as(id + " EN").isNotBlank();
			assertThat(resolver.thai(id, Map.of())).as(id + " TH").isNotBlank();
		}
	}

	@Test
	void placeholdersAreFilledInBothLanguages() {
		Map<String, String> placeholders = Map.of("field", "case.entry.dpd", "min", "1", "max", "365");

		assertThat(resolver.english("MSG-GEN-002", placeholders))
			.isEqualTo("case.entry.dpd must be between 1 and 365.");
		assertThat(resolver.thai("MSG-GEN-002", placeholders)).contains("case.entry.dpd").contains("1").contains("365");
	}

	@Test
	void theReadinessMessageNamesTheKeyAndEnvironment() {
		assertThat(resolver.english("MSG-P3-032", Map.of("name", "refdata.cache.ttl-seconds", "environment", "UAT")))
			.contains("refdata.cache.ttl-seconds")
			.contains("UAT");
	}

	@Test
	void anUnknownIdFailsLoudly() {
		assertThatThrownBy(() -> resolver.english("MSG-NOT-A-MESSAGE", Map.of()))
			.isInstanceOf(IllegalArgumentException.class)
			.hasMessageContaining("MSG-NOT-A-MESSAGE");
		assertThatThrownBy(() -> resolver.thai(null, Map.of())).isInstanceOf(IllegalArgumentException.class);
	}

	@Test
	void everyMessageKeepsItsPlaceholdersInBothLanguages() {
		for (String id : IDS) {
			String english = resolver.english(id, Map.of());
			String thai = resolver.thai(id, Map.of());
			assertThat(placeholdersOf(thai)).as(id + " TH placeholders").containsExactlyInAnyOrderElementsOf(
					placeholdersOf(english));
		}
	}

	private static List<String> placeholdersOf(String text) {
		List<String> found = new java.util.ArrayList<>();
		java.util.regex.Matcher matcher = java.util.regex.Pattern.compile("\\{([a-zA-Z]+)\\}").matcher(text);
		while (matcher.find()) {
			if (!found.contains(matcher.group(1))) {
				found.add(matcher.group(1));
			}
		}
		return found;
	}
}
