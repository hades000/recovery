package th.co.scb.ace.demo.recovery.casewf.config;

import java.io.IOException;
import java.io.InputStream;
import java.io.UncheckedIOException;
import java.time.Instant;
import java.time.LocalDate;
import java.util.ArrayList;
import java.util.List;
import java.util.Map;
import java.util.Optional;
import java.util.UUID;

import org.springframework.boot.autoconfigure.condition.ConditionalOnProperty;
import org.springframework.context.ApplicationEventPublisher;
import java.sql.SQLException;

import org.hibernate.exception.ConstraintViolationException;
import org.springframework.dao.DataIntegrityViolationException;
import org.springframework.http.HttpStatus;
import org.springframework.stereotype.Component;
import org.springframework.transaction.PlatformTransactionManager;
import org.springframework.transaction.TransactionDefinition;
import org.springframework.transaction.support.TransactionSynchronization;
import org.springframework.transaction.support.TransactionSynchronizationManager;
import org.springframework.transaction.support.TransactionTemplate;

import th.co.scb.ace.demo.recovery.access.api.ApiError;
import th.co.scb.ace.demo.recovery.access.api.ApiProblemException;
import th.co.scb.ace.demo.recovery.casewf.config.api.BusinessDateProvider;
import th.co.scb.ace.demo.recovery.casewf.config.api.ParameterLoadHandler;
import th.co.scb.ace.demo.recovery.casewf.config.api.ParameterLoadResult;
import th.co.scb.ace.demo.recovery.casewf.config.api.ParameterVersionApproved;

/**
 * The PARAMETER branch of the reference-load pipeline (SPEC-RWB-E1-042-012..-019; D-RUN-10,
 * D-RUN-20). Each of {@code load}, {@code approve} and {@code rollback} runs in its own
 * {@code REQUIRES_NEW} transaction, so RWB-E1-043's endpoint gets a committed result or an exception
 * and a caller's rollback cannot undo a recorded approval. Approve is maker-checker, writes the
 * decision inside the transaction, and publishes {@link ParameterVersionApproved} after commit.
 */
@Component
@ConditionalOnProperty(prefix = "rwb.p3", name = "configservice", havingValue = "true")
class ParameterLoadHandlerImpl implements ParameterLoadHandler {

	private static final String DECISION_CODE = "AC-VERS";

	/** The partial unique index that allows one approved version per (key, environment, date). */
	private static final String APPROVAL_UNIQUE_INDEX = "ux_parameter_value_approved_from";

	/** SQLState of a PostgreSQL unique violation. */
	private static final String UNIQUE_VIOLATION = "23505";

	private final ParameterValueRepository values;

	private final ParameterLoadValidator validator;

	private final VersionDecisionRecorder recorder;

	private final BusinessDateProvider businessDate;

	private final ApplicationEventPublisher events;

	private final ParameterCache cache;

	private final TransactionTemplate requiresNew;

	private final TransactionTemplate readOnly;

	ParameterLoadHandlerImpl(ParameterValueRepository values, ParameterLoadValidator validator,
			VersionDecisionRecorder recorder, BusinessDateProvider businessDate, ApplicationEventPublisher events,
			ParameterCache cache, PlatformTransactionManager transactionManager) {
		this.values = values;
		this.validator = validator;
		this.recorder = recorder;
		this.businessDate = businessDate;
		this.events = events;
		this.cache = cache;
		this.requiresNew = new TransactionTemplate(transactionManager);
		this.requiresNew.setPropagationBehavior(TransactionDefinition.PROPAGATION_REQUIRES_NEW);
		this.readOnly = new TransactionTemplate(transactionManager);
		this.readOnly.setPropagationBehavior(TransactionDefinition.PROPAGATION_REQUIRES_NEW);
		this.readOnly.setReadOnly(true);
	}

	@Override
	public ParameterLoadResult load(InputStream csv, LocalDate validFrom, UUID authorUserId) {
		if (authorUserId == null) {
			throw new IllegalArgumentException("authorUserId is required");
		}
		List<ParameterContentHash.Row> rows = validator.validate(read(csv), validFrom, businessDate.today());
		String hash = ParameterContentHash.of(rows);
		try {
			return requiresNew.execute(status -> {
				// SPEC-013: two identical loads are serialised, so the second one sees the first.
				values.advisoryLock(validFrom + "|" + hash);
				// Check 11 (the identical repeat) comes before check 12, so an approved load repeats
				// instead of being refused by its own approved rows (§12.5, code-gate CODE-001).
				List<ParameterValueEntity> existing = values.findByContent(validFrom, hash);
				if (!existing.isEmpty()) {
					return result(existing, true);
				}
				validator.validateApprovalWindow(rows, validFrom);
				return write(rows, validFrom, authorUserId, hash);
			});
		}
		catch (DataIntegrityViolationException ex) {
			return readOnly.execute(status -> {
				List<ParameterValueEntity> found = values.findByContent(validFrom, hash);
				if (!found.isEmpty()) {
					return result(found, true);
				}
				throw new ApiProblemException(HttpStatus.CONFLICT, "MSG-GEN-004", Map.of(), null, null, null);
			});
		}
	}

	private ParameterLoadResult write(List<ParameterContentHash.Row> rows, LocalDate validFrom, UUID authorUserId,
			String hash) {
		UUID loadId = UUID.randomUUID();
		Instant now = Instant.now();
		List<ParameterValueEntity> written = new ArrayList<>();
		for (ParameterContentHash.Row row : rows) {
			ParameterValueEntity entity = new ParameterValueEntity();
			entity.id = UUID.randomUUID();
			entity.paramKey = row.key();
			entity.environment = row.environment();
			entity.paramValue = row.value();
			entity.productGroup = null;
			entity.versionNo = values.maxVersionNo(row.key(), row.environment()) + 1;
			entity.validFrom = validFrom;
			entity.validTo = null;
			entity.status = "VALIDATED";
			entity.authorUserId = authorUserId;
			entity.approverUserId = null;
			entity.approvedAt = null;
			entity.active = true;
			entity.state = null;
			entity.version = 1;
			entity.createdAt = now;
			entity.createdBy = authorUserId;
			entity.updatedAt = now;
			entity.updatedBy = authorUserId;
			entity.loadId = loadId;
			entity.contentHash = hash;
			entity.rollbackReason = null;
			written.add(entity);
			values.save(entity);
		}
		return result(written, false);
	}

	@Override
	public ParameterLoadResult approve(UUID loadId, UUID approverUserId) {
		if (loadId == null || approverUserId == null) {
			throw new IllegalArgumentException("loadId and approverUserId are required");
		}
		LocalDate today = businessDate.today();
		try {
			return approveInTransaction(loadId, approverUserId, today);
		}
		catch (RuntimeException ex) {
			// SPEC-014: a concurrent approval loses the unique index race and gets 409 MSG-GEN-004.
			if (isApprovalConflict(ex)) {
				throw new ApiProblemException(HttpStatus.CONFLICT, "MSG-GEN-004", Map.of(), null, null, ex);
			}
			throw ex;
		}
	}

	private ParameterLoadResult approveInTransaction(UUID loadId, UUID approverUserId, LocalDate today) {
		return requiresNew.execute(status -> {
			lockKeyEnvironments(loadId);
			List<ParameterValueEntity> rows = values.lockByLoadId(loadId);
			if (rows.isEmpty()) {
				throw notInScope();
			}
			if (!"VALIDATED".equals(rows.get(0).status)) {
				throw new ApiProblemException(HttpStatus.CONFLICT, "MSG-GEN-004", Map.of(), null, null, null);
			}
			if (rows.stream().anyMatch(row -> approverUserId.equals(row.authorUserId))) {
				throw new ApiProblemException(HttpStatus.CONFLICT, "MSG-P7-002", Map.of(), null, null, null);
			}
			LocalDate validFrom = rows.get(0).validFrom;
			if (validFrom.isBefore(today)) {
				throw new ApiProblemException(HttpStatus.CONFLICT, "MSG-P3-027",
						Map.of("table", TABLE, "check", "valid from is before the business date"), null, null, null);
			}
			for (ParameterValueEntity row : rows) {
				if (values.countApprovedFrom(row.paramKey, row.environment, validFrom) > 0) {
					throw new ApiProblemException(HttpStatus.CONFLICT, "MSG-P3-027",
							Map.of("table", TABLE, "check",
									"an approved version from " + validFrom + " exists for " + row.paramKey + " "
											+ row.environment),
							null, null, null);
				}
			}
			Instant now = Instant.now();
			for (ParameterValueEntity row : rows) {
				row.status = "APPROVED";
				row.approverUserId = approverUserId;
				row.approvedAt = now;
				row.updatedAt = now;
				row.updatedBy = approverUserId;
				row.version = row.version + 1;
			}
			values.flush();
			ParameterValidity.recompute(values.findApproved(keys(rows)));
			recordDecision("APPROVED", loadId, rows, validFrom, approverUserId);
			ParameterVersionApproved approved = approved(loadId, rows);
			// SEC-042-04: the event is published after the approval commits, never inside the transaction.
			afterCommit(() -> {
				approved.versions().forEach(version -> cache.invalidate(version.paramKey(), version.environment()));
				events.publishEvent(approved);
			});
			return result(rows, false);
		});
	}

	@Override
	public ParameterLoadResult rollback(UUID loadId, String reason, UUID userId) {
		if (loadId == null || userId == null) {
			throw new IllegalArgumentException("loadId and userId are required");
		}
		String trimmed = ParameterLoadValidator.validateReason(reason);
		return requiresNew.execute(status -> {
			lockKeyEnvironments(loadId);
			List<ParameterValueEntity> rows = values.lockByLoadId(loadId);
			if (rows.isEmpty()) {
				throw notInScope();
			}
			if (!"APPROVED".equals(rows.get(0).status)) {
				throw new ApiProblemException(HttpStatus.CONFLICT, "MSG-P3-027",
						Map.of("table", TABLE, "check", "only an approved load can be rolled back"), null, null, null);
			}
			for (ParameterValueEntity row : rows) {
				if (values.countApprovedBefore(row.paramKey, row.environment, row.validFrom) == 0) {
					throw new ApiProblemException(HttpStatus.CONFLICT, "MSG-P3-015", Map.of("table", TABLE), null,
							null, null);
				}
			}
			Instant now = Instant.now();
			LocalDate validFrom = rows.get(0).validFrom;
			for (ParameterValueEntity row : rows) {
				row.status = "ROLLED_BACK";
				row.rollbackReason = trimmed;
				row.updatedAt = now;
				row.updatedBy = userId;
				row.version = row.version + 1;
			}
			values.flush();
			ParameterValidity.recompute(values.findApproved(keys(rows)));
			// REVIEW-001 M5, CG-R001-01 (AGENTS 3.4): the rollback is a decision too, recorded with the
			// outcome ROLLED_BACK. No rollback decision code exists in LOV-DECISION, so the version
			// decision code is kept (assumption A-01; open item proposed in shared-updates.md).
			recordDecision("ROLLED_BACK", loadId, rows, validFrom, userId);
			afterCommit(cache::invalidateAll);
			return result(rows, false);
		});
	}

	/**
	 * REVIEW-001 H1: approvals and rollbacks of one (key, environment) run one at a time. The locks are
	 * taken before any row is read, so the date checks and the valid_to recomputation see the other
	 * transaction's committed result. They are taken in ascending order of the lock key itself
	 * (CG-R001-02), so two transactions cannot wait on each other's advisory locks.
	 */
	private void lockKeyEnvironments(UUID loadId) {
		values.keyEnvironmentLocksOf(loadId).forEach(values::advisoryLock);
	}

	/** Writes the decision inside the transaction; a recorder failure is 503 MSG-P7-003 and rolls back. */
	private void recordDecision(String outcome, UUID loadId, List<ParameterValueEntity> rows, LocalDate validFrom,
			UUID userId) {
		try {
			recorder.recorded(DECISION_CODE, outcome, TABLE, loadId, keys(rows), validFrom, userId);
		}
		catch (RuntimeException ex) {
			throw new ApiProblemException(HttpStatus.SERVICE_UNAVAILABLE, "MSG-P7-003", Map.of(), null, null, ex);
		}
	}

	@Override
	public Optional<ParameterLoadResult> find(UUID loadId) {
		if (loadId == null) {
			return Optional.empty();
		}
		List<ParameterValueEntity> rows = values.findByLoadId(loadId);
		return rows.isEmpty() ? Optional.empty() : Optional.of(result(rows, false));
	}

	private ParameterVersionApproved approved(UUID loadId, List<ParameterValueEntity> rows) {
		List<ParameterVersionApproved.Version> versions = rows.stream()
			.map(row -> new ParameterVersionApproved.Version(row.paramKey, row.environment, row.versionNo))
			.toList();
		return new ParameterVersionApproved(loadId, keys(rows), rows.get(0).validFrom, versions, Instant.now());
	}

	private static ParameterLoadResult result(List<ParameterValueEntity> rows, boolean repeat) {
		ParameterValueEntity first = rows.get(0);
		// The rows of one load always share a status: approve and rollback change them together.
		return new ParameterLoadResult(first.loadId, TABLE, first.validFrom, first.status, rows.size(), repeat);
	}

	private static List<String> keys(List<ParameterValueEntity> rows) {
		return rows.stream().map(row -> row.paramKey).distinct().toList();
	}

	private static ApiProblemException notInScope() {
		return new ApiProblemException(ApiError.NOT_IN_SCOPE, Map.of(), null);
	}

	private static byte[] read(InputStream csv) {
		if (csv == null) {
			return new byte[0];
		}
		try (InputStream in = csv) {
			return in.readAllBytes();
		}
		catch (IOException ex) {
			throw new UncheckedIOException(ex);
		}
	}

	/**
	 * True only for the approval unique index: SQLState {@code 23505} (unique violation) and the
	 * constraint {@code ux_parameter_value_approved_from}. Any other integrity failure — a check
	 * constraint, an unrelated unique index, a recorder that itself stores data — keeps its own
	 * mapping, so the recorder failure still answers 503 MSG-P7-003 (Ponytail New 10).
	 */
	private static boolean isApprovalConflict(Throwable failure) {
		boolean uniqueViolation = false;
		boolean approvalIndex = false;
		for (Throwable cause = failure; cause != null; cause = cause.getCause()) {
			if (cause instanceof SQLException sql && UNIQUE_VIOLATION.equals(sql.getSQLState())) {
				uniqueViolation = true;
			}
			String message = cause.getMessage();
			if (message != null && message.contains(APPROVAL_UNIQUE_INDEX)) {
				approvalIndex = true;
			}
			if (cause instanceof ConstraintViolationException constraint
					&& APPROVAL_UNIQUE_INDEX.equals(constraint.getConstraintName())) {
				approvalIndex = true;
			}
		}
		return uniqueViolation && approvalIndex;
	}

	/** Runs the action after the handler's own transaction commits; it is only called inside one. */
	private static void afterCommit(Runnable action) {
		TransactionSynchronizationManager.registerSynchronization(new TransactionSynchronization() {
			@Override
			public void afterCommit() {
				action.run();
			}
		});
	}
}