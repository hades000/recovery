package th.co.scb.ace.demo.recovery.casewf.config;

import static org.assertj.core.api.Assertions.assertThat;
import static org.assertj.core.api.Assertions.assertThatThrownBy;
import static org.mockito.ArgumentMatchers.any;
import static org.mockito.ArgumentMatchers.anyString;
import static org.mockito.Mockito.mock;
import static org.mockito.Mockito.when;

import java.nio.charset.StandardCharsets;
import java.time.LocalDate;
import java.util.List;

import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;

import th.co.scb.ace.demo.recovery.access.api.ApiProblemException;

/**
 * TC-E1-042-05, -06, -18, -23, -36 and -39 (SPEC-RWB-E1-042-012, -014, -015): each of the load checks
 * refuses the whole load with its message ID, status and placeholders, in the order of §12.5.
 */
class ParameterLoadValidatorTest {

	private static final LocalDate TODAY = LocalDate.of(2026, 12, 1);

	private ParameterValueRepository values;

	private ParameterLoadValidator validator;

	@BeforeEach
	void setUp() {
		values = mock(ParameterValueRepository.class);
		when(values.countApprovedFrom(anyString(), anyString(), any(LocalDate.class))).thenReturn(0L);
		validator = new ParameterLoadValidator(values);
	}

	@Test
	void outOfRangeRefusesWithGen002() {
		assertThatThrownBy(() -> validate(TODAY, "case.entry.dpd,PROD,400"))
			.isInstanceOf(ApiProblemException.class)
			.satisfies(ex -> {
				ApiProblemException problem = (ApiProblemException) ex;
				assertThat(problem.messageId()).isEqualTo("MSG-GEN-002");
				assertThat(problem.status().value()).isEqualTo(422);
				assertThat(problem.placeholders()).containsEntry("field", "case.entry.dpd")
					.containsEntry("min", "1")
					.containsEntry("max", "365");
			});
	}

	@Test
	void wrongTypeRefusesWithP1002() {
		assertThatThrownBy(() -> validate(TODAY, "case.entry.dpd,PROD,ninety"))
			.isInstanceOf(ApiProblemException.class)
			.satisfies(ex -> {
				ApiProblemException problem = (ApiProblemException) ex;
				assertThat(problem.messageId()).isEqualTo("MSG-P1-002");
				assertThat(problem.placeholders()).containsEntry("source", "PARAMETER")
					.containsEntry("date", "2026-12-01")
					.containsEntry("check", "value is not INTEGER");
			});
	}

	@Test
	void unknownKeyEmptyFileAndPastValidFrom() {
		assertThatThrownBy(() -> validate(TODAY, "not.a.key,PROD,1"))
			.isInstanceOf(ApiProblemException.class)
			.satisfies(ex -> assertThat(((ApiProblemException) ex).messageId()).isEqualTo("MSG-P1-002"));
		assertThatThrownBy(() -> validator.validate(new byte[0], TODAY, TODAY))
			.isInstanceOf(ApiProblemException.class)
			.satisfies(ex -> assertThat(((ApiProblemException) ex).placeholders()).containsEntry("field", "file"));
		assertThatThrownBy(() -> validate(TODAY.minusDays(1), "case.entry.dpd,PROD,90"))
			.isInstanceOf(ApiProblemException.class)
			.satisfies(ex -> {
				ApiProblemException problem = (ApiProblemException) ex;
				assertThat(problem.messageId()).isEqualTo("MSG-P3-027");
				assertThat(problem.placeholders()).containsEntry("table", "PARAMETER");
			});
	}

	@Test
	void validFromBeforeTheBusinessDateIsRefused() {
		assertThatThrownBy(() -> validate(TODAY.minusDays(1), "case.entry.dpd,PROD,90"))
			.isInstanceOf(ApiProblemException.class)
			.satisfies(ex -> assertThat(((ApiProblemException) ex).status().value()).isEqualTo(422));
	}

	@Test
	void blankReasonIsRefused() {
		assertThatThrownBy(() -> ParameterLoadValidator.validateReason("   "))
			.isInstanceOf(ApiProblemException.class)
			.satisfies(ex -> {
				ApiProblemException problem = (ApiProblemException) ex;
				assertThat(problem.messageId()).isEqualTo("MSG-GEN-001");
				assertThat(problem.field()).isEqualTo("reason");
			});
		assertThatThrownBy(() -> ParameterLoadValidator.validateReason(null))
			.isInstanceOf(ApiProblemException.class);
	}

	@Test
	void reasonAtFourHundredIsAcceptedAndFourHundredAndOneIsRefused() {
		String atLimit = "x".repeat(400);

		assertThat(ParameterLoadValidator.validateReason("  " + atLimit + "  ")).hasSize(400);
		assertThatThrownBy(() -> ParameterLoadValidator.validateReason("x".repeat(401)))
			.isInstanceOf(ApiProblemException.class);
	}

	@Test
	void aKeyThatIsNotLoadableIsRefused() {
		assertThatThrownBy(() -> validate(TODAY, "ace.db.password,PROD,x"))
			.isInstanceOf(ApiProblemException.class)
			.satisfies(ex -> assertThat(((ApiProblemException) ex).placeholders().get("check"))
				.contains("cannot be loaded"));
		assertThatThrownBy(() -> validate(TODAY, "ENTRY_DPD,PROD,1"))
			.isInstanceOf(ApiProblemException.class);
		assertThatThrownBy(() -> validate(TODAY, "temporal.target,PROD,host:7233"))
			.isInstanceOf(ApiProblemException.class);
	}

	@Test
	void anEnvironmentNotListedIsRefused() {
		assertThatThrownBy(() -> validate(TODAY, "case.entry.dpd,PRD,90"))
			.isInstanceOf(ApiProblemException.class)
			.satisfies(ex -> assertThat(((ApiProblemException) ex).placeholders().get("check"))
				.contains("environment PRD is not listed"));
	}

	@Test
	void aBlankValueAndADuplicateRowAreRefused() {
		assertThatThrownBy(() -> validate(TODAY, "case.entry.dpd,PROD,  "))
			.isInstanceOf(ApiProblemException.class)
			.satisfies(ex -> assertThat(((ApiProblemException) ex).field()).isEqualTo("value of case.entry.dpd"));
		assertThatThrownBy(() -> validate(TODAY, "case.entry.dpd,PROD,90", "case.entry.dpd,PROD,91"))
			.isInstanceOf(ApiProblemException.class)
			.satisfies(ex -> assertThat(((ApiProblemException) ex).placeholders().get("check"))
				.contains("duplicate row"));
	}

	@Test
	void anApprovedVersionOnOrAfterTheDateIsARefusal409() {
		List<ParameterContentHash.Row> rows = validate(TODAY, "case.entry.dpd,PROD,90");
		when(values.countApprovedFrom(anyString(), anyString(), any(LocalDate.class))).thenReturn(1L);

		// Check 12 runs after the identical-repeat lookup (§12.5, code-gate CODE-001).
		assertThatThrownBy(() -> validator.validateApprovalWindow(rows, TODAY))
			.isInstanceOf(ApiProblemException.class)
			.satisfies(ex -> {
				ApiProblemException problem = (ApiProblemException) ex;
				assertThat(problem.status().value()).isEqualTo(409);
				assertThat(problem.messageId()).isEqualTo("MSG-P3-027");
			});
	}

	@Test
	void aGoodFileIsAcceptedAndTrimmed() {
		List<ParameterContentHash.Row> rows = validate(TODAY, "case.entry.dpd,PROD, 90 ", "rules.testcases.min,SIT,60");

		assertThat(rows).containsExactly(new ParameterContentHash.Row("case.entry.dpd", "PROD", "90"),
				new ParameterContentHash.Row("rules.testcases.min", "SIT", "60"));
	}

	/** Ponytail Should 2: the column is varchar(400); a longer value is a 422 length refusal. */
	@Test
	void aValueLongerThanTheColumnIsRefused() {
		String tooLong = "q".repeat(401);

		assertThatThrownBy(() -> validate(TODAY, "temporal.taskqueue.platform,PROD," + tooLong))
			.isInstanceOf(ApiProblemException.class)
			.satisfies(ex -> {
				ApiProblemException problem = (ApiProblemException) ex;
				assertThat(problem.messageId()).isEqualTo("MSG-P1-002");
				assertThat(problem.status().value()).isEqualTo(422);
				assertThat(problem.placeholders()).containsEntry("source", "PARAMETER")
					.containsEntry("check", "value is longer than 400 characters");
			});
	}

	/** Ponytail Should 8: a malformed UTF-8 byte is refused, not replaced with U+FFFD. */
	@Test
	void aNonUtf8FileIsRefused() {
		byte[] body = "key,environment,value\ntemporal.taskqueue.platform,PROD,q".getBytes(StandardCharsets.UTF_8);
		byte[] invalid = new byte[body.length + 1];
		System.arraycopy(body, 0, invalid, 0, body.length);
		invalid[body.length] = (byte) 0xC3;

		assertThatThrownBy(() -> validator.validate(invalid, TODAY, TODAY))
			.isInstanceOf(ApiProblemException.class)
			.satisfies(ex -> {
				ApiProblemException problem = (ApiProblemException) ex;
				assertThat(problem.messageId()).isEqualTo("MSG-P1-002");
				assertThat(problem.status().value()).isEqualTo(422);
				assertThat(problem.placeholders().get("check")).contains("UTF-8");
			});
	}

	@Test
	void aClosedRangeIsAcceptedAtBothEnds() {
		assertThat(validate(TODAY, "case.entry.dpd,PROD,1")).hasSize(1);
		assertThat(validate(TODAY, "case.entry.dpd,PROD,365")).hasSize(1);
		assertThatThrownBy(() -> validate(TODAY, "case.entry.dpd,PROD,0"))
			.isInstanceOf(ApiProblemException.class);
		assertThatThrownBy(() -> validate(TODAY, "case.entry.dpd,PROD,366"))
			.isInstanceOf(ApiProblemException.class);
	}

	private List<ParameterContentHash.Row> validate(LocalDate validFrom, String... lines) {
		String text = "key,environment,value\n" + String.join("\n", lines) + "\n";
		return validator.validate(text.getBytes(StandardCharsets.UTF_8), validFrom, TODAY);
	}
}
