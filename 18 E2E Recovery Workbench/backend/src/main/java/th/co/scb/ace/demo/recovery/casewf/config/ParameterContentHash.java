package th.co.scb.ace.demo.recovery.casewf.config;

import java.nio.charset.StandardCharsets;
import java.security.MessageDigest;
import java.security.NoSuchAlgorithmException;
import java.util.Comparator;
import java.util.HexFormat;
import java.util.List;

/**
 * The canonical form and SHA-256 of a parameter load (SPEC-RWB-E1-042-013): the rows sorted by key,
 * then environment, each line {@code key|environment|value}, joined with a newline, on the unquoted
 * value. Lower-case hex.
 */
final class ParameterContentHash {

	/** One load row after the CSV reader unquoted it. */
	record Row(String key, String environment, String value) {
	}

	private ParameterContentHash() {
	}

	static String of(List<Row> rows) {
		List<Row> sorted = rows.stream()
			.sorted(Comparator.comparing(Row::key).thenComparing(Row::environment))
			.toList();
		StringBuilder canonical = new StringBuilder();
		for (Row row : sorted) {
			if (!canonical.isEmpty()) {
				canonical.append('\n');
			}
			canonical.append(row.key()).append('|').append(row.environment()).append('|').append(row.value());
		}
		return sha256(canonical.toString());
	}

	private static String sha256(String text) {
		try {
			MessageDigest digest = MessageDigest.getInstance("SHA-256");
			return HexFormat.of().formatHex(digest.digest(text.getBytes(StandardCharsets.UTF_8)));
		}
		catch (NoSuchAlgorithmException ex) {
			throw new IllegalStateException(ex);
		}
	}
}