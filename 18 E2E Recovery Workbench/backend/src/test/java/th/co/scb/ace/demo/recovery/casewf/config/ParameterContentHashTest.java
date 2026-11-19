package th.co.scb.ace.demo.recovery.casewf.config;

import static org.assertj.core.api.Assertions.assertThat;

import java.util.List;

import org.junit.jupiter.api.Test;

/**
 * TC-E1-042-16 (SPEC-RWB-E1-042-013): the canonical form sorts by key then environment, hashes the
 * unquoted value as {@code key|environment|value} lines joined with a newline, and returns lower-case
 * hex.
 */
class ParameterContentHashTest {

	@Test
	void quotedCodeListHashesOnTheUnquotedValue() {
		String withCommas = ParameterContentHash.of(List.of(
				new ParameterContentHash.Row("servicelevel.required-statuses", "DEV", "NEW,ASSIGNED,IN_PROGRESS")));

		assertThat(withCommas).hasSize(64).matches("^[0-9a-f]{64}$");
		assertThat(withCommas).isEqualTo(ParameterContentHash.of(
				List.of(new ParameterContentHash.Row("servicelevel.required-statuses", "DEV",
						"NEW,ASSIGNED,IN_PROGRESS"))));
	}

	@Test
	void theOrderOfTheRowsDoesNotChangeTheHash() {
		ParameterContentHash.Row first = new ParameterContentHash.Row("case.entry.dpd", "DEV", "90");
		ParameterContentHash.Row second = new ParameterContentHash.Row("case.entry.dpd", "SIT", "30");

		assertThat(ParameterContentHash.of(List.of(first, second)))
			.isEqualTo(ParameterContentHash.of(List.of(second, first)));
	}

	@Test
	void aDifferentValueChangesTheHash() {
		assertThat(ParameterContentHash.of(List.of(new ParameterContentHash.Row("case.entry.dpd", "DEV", "90"))))
			.isNotEqualTo(ParameterContentHash.of(
					List.of(new ParameterContentHash.Row("case.entry.dpd", "DEV", "91"))));
	}

	@Test
	void theHashIsLowercaseHexOfTheCanonicalText() {
		String empty = ParameterContentHash.of(List.of());

		assertThat(empty).isEqualTo("e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855");
	}
}