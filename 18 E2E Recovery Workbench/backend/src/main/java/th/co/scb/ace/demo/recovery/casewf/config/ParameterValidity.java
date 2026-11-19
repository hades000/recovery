package th.co.scb.ace.demo.recovery.casewf.config;

import java.time.LocalDate;
import java.util.ArrayList;
import java.util.Comparator;
import java.util.LinkedHashMap;
import java.util.List;
import java.util.Map;
import java.util.Objects;

/**
 * Recomputes {@code valid_to} after every approval or rollback (SPEC-RWB-E1-042-014, -015): for each
 * (key, environment, product group) the APPROVED rows are ordered by {@code valid_from}; each row's
 * {@code valid_to} is the next row's {@code valid_from} minus one day and the last row's is null.
 * Rows in other statuses keep null.
 */
final class ParameterValidity {

	private ParameterValidity() {
	}

	static void recompute(List<ParameterValueEntity> rows) {
		Map<String, List<ParameterValueEntity>> groups = new LinkedHashMap<>();
		for (ParameterValueEntity row : rows) {
			if (!"APPROVED".equals(row.status)) {
				row.validTo = null;
				continue;
			}
			groups.computeIfAbsent(groupKey(row), key -> new ArrayList<>()).add(row);
		}
		for (List<ParameterValueEntity> group : groups.values()) {
			List<ParameterValueEntity> ordered = group.stream()
				.sorted(Comparator.comparing(row -> row.validFrom))
				.toList();
			for (int index = 0; index < ordered.size(); index++) {
				ParameterValueEntity row = ordered.get(index);
				if (index + 1 < ordered.size()) {
					LocalDate nextFrom = ordered.get(index + 1).validFrom;
					row.validTo = nextFrom.minusDays(1);
				}
				else {
					row.validTo = null;
				}
			}
		}
	}

	static String groupKey(ParameterValueEntity row) {
		return row.paramKey + "|" + row.environment + "|" + Objects.toString(row.productGroup, "");
	}
}