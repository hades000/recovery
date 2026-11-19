package recovery.casewf.caselist;

import java.util.Map;
import java.util.Optional;

/** Fixture for TC-E1-042-03 (g): Map.get and Optional.get are not key reads. Not compiled. */
public class LimitsReader {

	private final Map<String, Integer> limits = Map.of();

	int fromMap(String key) {
		return limits.get(key);
	}

	int fromOptional(Optional<Integer> value) {
		return value.get();
	}
}