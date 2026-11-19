package th.co.scb.ace.demo.recovery.casewf.config;

import static org.assertj.core.api.Assertions.assertThat;

import java.time.LocalDate;
import java.util.List;

import org.junit.jupiter.api.Test;

/**
 * TC-E1-042-10 and TC-E1-042-11 (SPEC-RWB-E1-042-014, -015): after an approval or a rollback the
 * earlier version is in force again, because each approved row's {@code valid_to} is the next row's
 * {@code valid_from} minus one day and the last row's is null.
 */
class ParameterValidityTest {

	@Test
	void recomputeMakesTheEarlierVersionInForce() {
		ParameterValueEntity first = row("v1", LocalDate.of(2026, 11, 2));
		ParameterValueEntity second = row("v2", LocalDate.of(2026, 12, 10));
		second.validTo = LocalDate.of(2026, 12, 20);

		ParameterValidity.recompute(List.of(second, first));

		assertThat(first.validTo).isEqualTo(LocalDate.of(2026, 12, 9));
		assertThat(second.validTo).isNull();
	}

	@Test
	void rowsInOtherStatusesKeepNull() {
		ParameterValueEntity rolledBack = row("v2", LocalDate.of(2026, 12, 10));
		rolledBack.status = "ROLLED_BACK";
		rolledBack.validTo = LocalDate.of(2026, 12, 20);

		ParameterValidity.recompute(List.of(rolledBack));

		assertThat(rolledBack.validTo).isNull();
	}

	@Test
	void aSingleApprovedRowHasNoEnd() {
		ParameterValueEntity only = row("v1", LocalDate.of(2026, 11, 2));

		ParameterValidity.recompute(List.of(only));

		assertThat(only.validTo).isNull();
	}

	@Test
	void theProductGroupAndEnvironmentSeparateTheGroups() {
		ParameterValueEntity global = row("v1", LocalDate.of(2026, 11, 2));
		ParameterValueEntity product = row("v1", LocalDate.of(2026, 11, 2));
		product.productGroup = "MORTGAGE";

		ParameterValidity.recompute(List.of(global, product));

		assertThat(global.validTo).isNull();
		assertThat(product.validTo).isNull();
	}

	private static ParameterValueEntity row(String value, LocalDate validFrom) {
		ParameterValueEntity row = new ParameterValueEntity();
		row.paramKey = "case.entry.dpd";
		row.environment = "PROD";
		row.paramValue = value;
		row.versionNo = 1;
		row.validFrom = validFrom;
		row.status = "APPROVED";
		return row;
	}
}