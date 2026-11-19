package th.co.scb.ace.demo.recovery.casewf.rules;

import static org.assertj.core.api.Assertions.assertThat;
import static org.assertj.core.api.Assertions.assertThatThrownBy;

import java.math.BigDecimal;
import java.util.Map;

import org.junit.jupiter.api.Test;

/**
 * RWB-TE-001 SPEC-024: the rule facts keep their typed reads, the single-decision rule and the
 * matched/no-match distinction.
 */
class RuleFactsTest {

	@Test
	void inputReadsNumbersTextAndFlags() {
		RuleInput input = RuleInput.of(Map.of("dpd", 30, "productGroup", "PL", "flagged", "true"));

		assertThat(input.num("dpd")).isEqualByComparingTo("30");
		assertThat(input.num("absent")).isNull();
		assertThat(input.text("productGroup")).isEqualTo("PL");
		assertThat(input.text("absent")).isNull();
		assertThat(input.flag("flagged")).isTrue();
		assertThat(input.has("dpd")).isTrue();
		assertThat(input.has("absent")).isFalse();
		assertThat(input.values()).containsEntry("productGroup", "PL");
	}

	@Test
	void inputAcceptsABigDecimalAsItIs() {
		assertThat(RuleInput.of(Map.of("amount", new BigDecimal("12.50"))).num("amount")).isEqualByComparingTo("12.50");
	}

	@Test
	void outcomeAcceptsOneDecisionAndRefusesASecond() {
		RuleOutcome outcome = new RuleOutcome();
		outcome.decide("R1");
		outcome.decide("R1");
		outcome.put("targetQueue", "rwb-case");

		assertThat(outcome.ruleId()).isEqualTo("R1");
		assertThat(outcome.outputs()).containsEntry("targetQueue", "rwb-case");
		assertThatThrownBy(() -> outcome.decide("R2")).isInstanceOf(IllegalStateException.class);
	}

	@Test
	void resultKnowsWhetherARuleMatched() {
		RuleResult noMatch = RuleResult.noMatch("P1", "v1");

		assertThat(noMatch.matched()).isFalse();
		assertThat(noMatch.ruleId()).isNull();
		assertThat(noMatch.packageCode()).isEqualTo("P1");
		assertThat(noMatch.packageVersion()).isEqualTo("v1");

		RuleResult matched = new RuleResult("P1", "v1", "R1", Map.of("outcome", "x"));

		assertThat(matched.matched()).isTrue();
		assertThat(matched.ruleId()).isEqualTo("R1");
		assertThat(matched.outputs()).containsEntry("outcome", "x");
	}
}
