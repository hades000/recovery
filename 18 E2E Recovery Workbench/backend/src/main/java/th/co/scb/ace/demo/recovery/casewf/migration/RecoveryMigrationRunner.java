package th.co.scb.ace.demo.recovery.casewf.migration;

import java.util.List;

import org.flywaydb.core.Flyway;
import org.flywaydb.core.api.FlywayException;
import org.flywaydb.core.api.MigrationInfo;
import org.flywaydb.core.api.callback.Callback;
import org.flywaydb.core.api.callback.Context;
import org.flywaydb.core.api.callback.Event;
import org.flywaydb.core.api.exception.FlywayValidateException;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

/**
 * SPEC-RWB-E1-044-003 (T-044-09, AC4, AC8): the migrate call is wrapped so a failure is reported as
 * one {@code MSG-P3-016 schema=<schema> object=<version>} line and then rethrown, so the context
 * fails and the service does not start.
 *
 * <p>The line holds the message ID and the two parameters only: no SQL and no credential
 * (CLAR-004, BS-4.6). The {@code object} choice follows the SPEC-003 table.
 */
final class RecoveryMigrationRunner {

	private static final Logger log = LoggerFactory.getLogger(RecoveryMigrationRunner.class);

	private static final String FALLBACK_OBJECT = "recoveryFlyway";

	private final Flyway flyway;

	private final RecoveryMigrationProperties properties;

	RecoveryMigrationRunner(Flyway flyway, RecoveryMigrationProperties properties) {
		this.flyway = flyway;
		this.properties = properties;
	}

	void migrate() {
		try {
			flyway.migrate();
		}
		catch (FlywayException failure) {
			log.error("MSG-P3-016 schema={} object={}", properties.schema(), failureObject(flyway, failure));
			throw failure;
		}
	}

	/**
	 * The version or versions concerned: the invalid migrations of a validation failure, otherwise
	 * the version of a migration that failed while running, otherwise the bean name for a failure
	 * with no version (connection refused, lock timeout, missing schema).
	 *
	 * <p>A validation failure with no invalid migration (a lower version pending under
	 * {@code outOfOrder(false)}) reports the first pending version. A migration that failed while
	 * running is named by {@link FailedVersion}, which Flyway calls through its public callback API
	 * (CONF2-E044-04). Any other {@link FlywayException} has no version, so it reports the bean name
	 * even when versions are pending (CONF-E044-04).
	 *
	 * <p>The lookup runs inside the failure handler, so a second failure (a broken database answers
	 * {@code info()} no better than {@code migrate()}) must never replace the original exception or
	 * skip the ERROR line: any runtime failure returns the fallback (SEC-044-04).
	 */
	static String failureObject(Flyway flyway, FlywayException failure) {
		try {
			if (failure instanceof FlywayValidateException) {
				List<String> versions = flyway.validateWithResult()
					.invalidMigrations
					.stream()
					.map(invalid -> invalid.version)
					.filter(version -> version != null && !version.isBlank())
					.map(RecoveryMigrationRunner::display)
					.distinct()
					.toList();
				if (!versions.isEmpty()) {
					return String.join(",", versions);
				}
				MigrationInfo[] pending = flyway.info().pending();
				if (pending.length > 0 && pending[0].getVersion() != null) {
					return versionOrFallback(pending[0].getVersion().getVersion());
				}
				return FALLBACK_OBJECT;
			}
			for (Callback callback : flyway.getConfiguration().getCallbacks()) {
				if (callback instanceof FailedVersion failed) {
					return versionOrFallback(failed.version);
				}
			}
		}
		catch (RuntimeException ex) {
			return FALLBACK_OBJECT;
		}
		return FALLBACK_OBJECT;
	}

	private static String versionOrFallback(String version) {
		return version != null && !version.isBlank() ? display(version) : FALLBACK_OBJECT;
	}

	/**
	 * Records the version of the migration that failed while running. Flyway fires
	 * {@link Event#AFTER_EACH_MIGRATE_ERROR} with that migration's info before it throws, so the runner
	 * reads the version here instead of from Flyway's internal exception type (CONF2-E044-04). It runs
	 * no SQL, so it may run inside the failed transaction.
	 */
	static final class FailedVersion implements Callback {

		private volatile String version;

		@Override
		public boolean supports(Event event, Context context) {
			return event == Event.AFTER_EACH_MIGRATE_ERROR;
		}

		@Override
		public boolean canHandleInTransaction(Event event, Context context) {
			return true;
		}

		@Override
		public void handle(Event event, Context context) {
			MigrationInfo info = context.getMigrationInfo();
			version = info == null || info.getVersion() == null ? null : info.getVersion().getVersion();
		}

		@Override
		public String getCallbackName() {
			return "recoveryFailedVersion";
		}

	}

	/** {@code V0002} is reported as {@code 2}, the version's value rather than its file padding. */
	private static String display(String version) {
		return java.util.Arrays.stream(version.split("\\."))
			.map(part -> !part.isEmpty() && part.chars().allMatch(Character::isDigit) ? new java.math.BigInteger(part).toString()
					: part)
			.collect(java.util.stream.Collectors.joining("."));
	}

}
