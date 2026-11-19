package th.co.scb.ace.demo.recovery.casewf.config;

import static org.assertj.core.api.Assertions.assertThat;
import static org.assertj.core.api.Assertions.assertThatThrownBy;
import static org.mockito.ArgumentMatchers.any;
import static org.mockito.ArgumentMatchers.anyList;
import static org.mockito.ArgumentMatchers.anyString;
import static org.mockito.ArgumentMatchers.eq;
import static org.mockito.Mockito.mock;
import static org.mockito.Mockito.never;
import static org.mockito.Mockito.verify;
import static org.mockito.Mockito.when;

import java.nio.charset.StandardCharsets;
import java.time.LocalDate;
import java.util.List;
import java.util.Optional;
import java.util.UUID;

import ch.qos.logback.classic.Logger;
import ch.qos.logback.classic.spi.ILoggingEvent;
import ch.qos.logback.core.read.ListAppender;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import org.slf4j.LoggerFactory;
import org.springframework.context.ApplicationEventPublisher;
import org.springframework.dao.DataIntegrityViolationException;

import th.co.scb.ace.demo.recovery.access.api.ApiProblemException;
import th.co.scb.ace.demo.recovery.casewf.config.api.BusinessDateProvider;
import th.co.scb.ace.demo.recovery.casewf.config.api.ParameterLoadResult;
import th.co.scb.ace.demo.recovery.casewf.config.api.ParameterVersionApproved;

/**
 * TC-E1-042-07, -16, -17, -19, -20, -28 and -29 (SPEC-RWB-E1-042-013..-019): maker-checker, the
 * single-use load, the identical repeat, the rollback refusals, the recorder failure and the one
 * event after commit — all through the handler with a real {@code TransactionTemplate}.
 */
class ParameterLoadHandlerTest {

	private static final LocalDate TODAY = LocalDate.of(2026, 12, 1);

	private static final UUID AUTHOR = UUID.fromString("00000000-0000-0000-0000-00000000a001");

	private static final UUID APPROVER = UUID.fromString("00000000-0000-0000-0000-00000000a002");

	private static final UUID LOAD = UUID.fromString("00000000-0000-0000-0000-00000000a00f");

	private ParameterValueRepository values;

	private ParameterLoadValidator validator;

	private VersionDecisionRecorder recorder;

	private ApplicationEventPublisher events;

	private ParameterLoadHandlerImpl handler;

	@BeforeEach
	void setUp() {
		values = mock(ParameterValueRepository.class);
		validator = mock(ParameterLoadValidator.class);
		recorder = mock(VersionDecisionRecorder.class);
		events = mock(ApplicationEventPublisher.class);
		BusinessDateProvider businessDate = () -> TODAY;
		handler = new ParameterLoadHandlerImpl(values, validator, recorder, businessDate, events,
				mock(ParameterCache.class), new StubTransactionManager());
	}

	@Test
	void authorCannotApprove() {
		when(values.lockByLoadId(LOAD)).thenReturn(List.of(row(AUTHOR, "VALIDATED", TODAY)));

		assertThatThrownBy(() -> handler.approve(LOAD, AUTHOR))
			.isInstanceOf(ApiProblemException.class)
			.satisfies(ex -> assertThat(((ApiProblemException) ex).messageId()).isEqualTo("MSG-P7-002"));
		verify(events, never()).publishEvent(any());
	}

	@Test
	void secondConcurrentApprovalIsRefused() {
		when(values.lockByLoadId(LOAD)).thenReturn(List.of(row(AUTHOR, "APPROVED", TODAY)));

		assertThatThrownBy(() -> handler.approve(LOAD, APPROVER))
			.isInstanceOf(ApiProblemException.class)
			.satisfies(ex -> assertThat(((ApiProblemException) ex).messageId()).isEqualTo("MSG-GEN-004"));
	}

	@Test
	void rollbackOfAValidatedLoadIsRefused() {
		when(values.lockByLoadId(LOAD)).thenReturn(List.of(row(AUTHOR, "VALIDATED", TODAY)));

		assertThatThrownBy(() -> handler.rollback(LOAD, "synthetic reason", APPROVER))
			.isInstanceOf(ApiProblemException.class)
			.satisfies(ex -> {
				ApiProblemException problem = (ApiProblemException) ex;
				assertThat(problem.messageId()).isEqualTo("MSG-P3-027");
				assertThat(problem.placeholders()).containsEntry("check", "only an approved load can be rolled back");
			});
	}

	@Test
	void rollbackWithNoEarlierVersionIsRefused() {
		when(values.lockByLoadId(LOAD)).thenReturn(List.of(row(AUTHOR, "APPROVED", TODAY)));
		when(values.countApprovedBefore(anyString(), anyString(), any(LocalDate.class))).thenReturn(0L);

		assertThatThrownBy(() -> handler.rollback(LOAD, "synthetic reason", APPROVER))
			.isInstanceOf(ApiProblemException.class)
			.satisfies(ex -> {
				ApiProblemException problem = (ApiProblemException) ex;
				assertThat(problem.messageId()).isEqualTo("MSG-P3-015");
				assertThat(problem.placeholders()).containsEntry("table", "PARAMETER");
			});
	}

	/** REVIEW-001 M5 (AGENTS 3.4): a rollback writes a decision record inside its transaction. */
	@Test
	void rollbackRecordsTheDecision() {
		ParameterValueEntity approved = row(AUTHOR, "APPROVED", TODAY);
		when(values.lockByLoadId(LOAD)).thenReturn(List.of(approved));
		when(values.countApprovedBefore(anyString(), anyString(), any(LocalDate.class))).thenReturn(1L);
		when(values.findApproved(anyList())).thenReturn(List.of());

		ParameterLoadResult result = handler.rollback(LOAD, "synthetic reason", APPROVER);

		verify(recorder)
			.recorded("AC-VERS", "ROLLED_BACK", "PARAMETER", LOAD, List.of("case.entry.dpd"), TODAY, APPROVER);
		assertThat(result.status()).isEqualTo("ROLLED_BACK");
		// REVIEW-001 M4: the rollback event had no listener and was removed.
		verify(events, never()).publishEvent(any());
	}

	/** REVIEW-001 M5: a rollback whose decision cannot be recorded is 503 MSG-P7-003, as for approve. */
	@Test
	void rollbackRecorderFailureIs503() {
		when(values.lockByLoadId(LOAD)).thenReturn(List.of(row(AUTHOR, "APPROVED", TODAY)));
		when(values.countApprovedBefore(anyString(), anyString(), any(LocalDate.class))).thenReturn(1L);
		when(values.findApproved(anyList())).thenReturn(List.of());
		RuntimeException failure = new IllegalStateException("synthetic recorder marker");
		org.mockito.Mockito.doThrow(failure)
			.when(recorder)
			.recorded(eq("AC-VERS"), eq("ROLLED_BACK"), eq("PARAMETER"), eq(LOAD), anyList(), eq(TODAY), eq(APPROVER));

		assertThatThrownBy(() -> handler.rollback(LOAD, "synthetic reason", APPROVER))
			.isInstanceOf(ApiProblemException.class)
			.satisfies(ex -> {
				ApiProblemException problem = (ApiProblemException) ex;
				assertThat(problem.messageId()).isEqualTo("MSG-P7-003");
				assertThat(problem.status().value()).isEqualTo(503);
				assertThat(problem.getCause()).isSameAs(failure);
			});
	}

	@Test
	void recorderFailureIs503AndRollsBack() {
		ParameterValueEntity pending = row(AUTHOR, "VALIDATED", TODAY);
		when(values.lockByLoadId(LOAD)).thenReturn(List.of(pending));
		when(values.findApproved(anyList())).thenReturn(List.of());
		RuntimeException failure = new IllegalStateException("synthetic recorder marker");
		org.mockito.Mockito.doThrow(failure)
			.when(recorder)
			.recorded(eq("AC-VERS"), eq("APPROVED"), eq("PARAMETER"), eq(LOAD), anyList(), eq(TODAY), eq(APPROVER));

		assertThatThrownBy(() -> handler.approve(LOAD, APPROVER))
			.isInstanceOf(ApiProblemException.class)
			.satisfies(ex -> {
				ApiProblemException problem = (ApiProblemException) ex;
				assertThat(problem.messageId()).isEqualTo("MSG-P7-003");
				assertThat(problem.status().value()).isEqualTo(503);
				assertThat(problem.placeholders()).isEmpty();
				assertThat(problem.detail()).isNull();
				assertThat(problem.getCause()).isSameAs(failure);
			});
		verify(events, never()).publishEvent(any());
	}

	/**
	 * REVIEW-001 CG-R001-01 (AGENTS 3.4): the decision record states what was decided. Through the
	 * interim recorder, the approval's line names APPROVED and the rollback's names ROLLED_BACK; the
	 * approver's user ID is not logged.
	 */
	@Test
	void theDecisionRecordNamesTheOutcome() {
		Logger logger = (Logger) LoggerFactory.getLogger(InterimVersionDecisionRecorder.class);
		ListAppender<ILoggingEvent> appender = new ListAppender<>();
		appender.start();
		logger.addAppender(appender);
		try {
			ParameterLoadHandlerImpl interim = new ParameterLoadHandlerImpl(values, validator,
					new InterimVersionDecisionRecorder(), () -> TODAY, events, mock(ParameterCache.class),
					new StubTransactionManager());
			when(values.findApproved(anyList())).thenReturn(List.of());
			when(values.lockByLoadId(LOAD)).thenReturn(List.of(row(AUTHOR, "VALIDATED", TODAY)));
			interim.approve(LOAD, APPROVER);
			when(values.lockByLoadId(LOAD)).thenReturn(List.of(row(AUTHOR, "APPROVED", TODAY)));
			when(values.countApprovedBefore(anyString(), anyString(), any(LocalDate.class))).thenReturn(1L);
			interim.rollback(LOAD, "synthetic reason", APPROVER);
		}
		finally {
			logger.detachAppender(appender);
		}

		assertThat(appender.list).extracting(ILoggingEvent::getFormattedMessage)
			.satisfiesExactly(approval -> assertThat(approval).contains("outcome=APPROVED"),
					rollback -> assertThat(rollback).contains("outcome=ROLLED_BACK"))
			.noneMatch(line -> line.contains(APPROVER.toString()));
	}

	@Test
	void interimRecorderIsCalledOnceInsideTheTransaction() {
		ParameterValueEntity pending = row(AUTHOR, "VALIDATED", TODAY);
		when(values.lockByLoadId(LOAD)).thenReturn(List.of(pending));
		when(values.findApproved(anyList())).thenReturn(List.of());

		ParameterLoadResult result = handler.approve(LOAD, APPROVER);

		verify(recorder)
			.recorded("AC-VERS", "APPROVED", "PARAMETER", LOAD, List.of("case.entry.dpd"), TODAY, APPROVER);
		assertThat(result.status()).isEqualTo("APPROVED");
		assertThat(pending.status).isEqualTo("APPROVED");
	}

	@Test
	void oneEventAfterCommitAndNoneOnRefusal() {
		ParameterValueEntity pending = row(AUTHOR, "VALIDATED", TODAY);
		when(values.lockByLoadId(LOAD)).thenReturn(List.of(pending));
		when(values.findApproved(anyList())).thenReturn(List.of());

		handler.approve(LOAD, APPROVER);

		verify(events).publishEvent(any(ParameterVersionApproved.class));
		org.mockito.Mockito.clearInvocations(events);
		when(values.lockByLoadId(LOAD)).thenReturn(List.of(row(AUTHOR, "VALIDATED", TODAY)));
		assertThatThrownBy(() -> handler.approve(LOAD, AUTHOR)).isInstanceOf(ApiProblemException.class);
		verify(events, never()).publishEvent(any());
	}

	/** CODE-001: the repeat lookup comes before check 12, so an approved load repeats. */
	@Test
	void anApprovedLoadRepeatsBeforeTheApprovedFromCheck() {
		List<ParameterContentHash.Row> rows = List.of(new ParameterContentHash.Row("case.entry.dpd", "PROD", "90"));
		when(validator.validate(any(), eq(TODAY), eq(TODAY))).thenReturn(rows);
		ParameterValueEntity approved = row(AUTHOR, "APPROVED", TODAY);
		approved.loadId = LOAD;
		when(values.findByContent(TODAY, ParameterContentHash.of(rows))).thenReturn(List.of(approved));

		ParameterLoadResult result = handler.load(csv("case.entry.dpd,PROD,90\n"), TODAY, AUTHOR);

		assertThat(result.repeat()).isTrue();
		assertThat(result.loadId()).isEqualTo(LOAD);
		assertThat(result.status()).isEqualTo("APPROVED");
		verify(validator, never()).validateApprovalWindow(anyList(), any());
	}

	/** CODE-001: a load that is not a repeat still meets check 12, and its refusal writes nothing. */
	@Test
	void aDifferentLoadStillMeetsTheApprovedFromCheck() {
		List<ParameterContentHash.Row> rows = List.of(new ParameterContentHash.Row("case.entry.dpd", "PROD", "91"));
		when(validator.validate(any(), eq(TODAY), eq(TODAY))).thenReturn(rows);
		when(values.findByContent(TODAY, ParameterContentHash.of(rows))).thenReturn(List.of());
		org.mockito.Mockito.doThrow(new ApiProblemException(org.springframework.http.HttpStatus.CONFLICT, "MSG-P3-027",
				java.util.Map.of(), null, null, null))
			.when(validator)
			.validateApprovalWindow(rows, TODAY);

		assertThatThrownBy(() -> handler.load(csv("case.entry.dpd,PROD,91\n"), TODAY, AUTHOR))
			.isInstanceOf(ApiProblemException.class)
			.satisfies(ex -> assertThat(((ApiProblemException) ex).messageId()).isEqualTo("MSG-P3-027"));
		verify(values, never()).save(any());
	}

	@Test
	void identicalRepeatReturnsTheExistingLoad() {
		List<ParameterContentHash.Row> rows = List.of(new ParameterContentHash.Row("case.entry.dpd", "PROD", "90"));
		when(validator.validate(any(), eq(TODAY), eq(TODAY))).thenReturn(rows);
		ParameterValueEntity existing = row(AUTHOR, "VALIDATED", TODAY);
		existing.loadId = LOAD;
		when(values.findByContent(TODAY, ParameterContentHash.of(rows))).thenReturn(List.of(existing));

		ParameterLoadResult result = handler.load(csv("case.entry.dpd,PROD,90\n"), TODAY, AUTHOR);

		assertThat(result.repeat()).isTrue();
		assertThat(result.loadId()).isEqualTo(LOAD);
		verify(values, never()).save(any());
	}

	@Test
	void aUniqueViolationBecomesAnIdenticalRepeat() {
		List<ParameterContentHash.Row> rows = List.of(new ParameterContentHash.Row("case.entry.dpd", "PROD", "90"));
		when(validator.validate(any(), eq(TODAY), eq(TODAY))).thenReturn(rows);
		when(values.findByContent(TODAY, ParameterContentHash.of(rows))).thenReturn(List.of());
		when(values.save(any())).thenThrow(new DataIntegrityViolationException("synthetic unique violation"));
		ParameterValueEntity existing = row(AUTHOR, "VALIDATED", TODAY);
		existing.loadId = LOAD;
		when(values.findByContent(TODAY, ParameterContentHash.of(rows))).thenReturn(List.of(), List.of(existing));

		ParameterLoadResult result = handler.load(csv("case.entry.dpd,PROD,90\n"), TODAY, AUTHOR);

		assertThat(result.repeat()).isTrue();
		assertThat(result.loadId()).isEqualTo(LOAD);
	}

	@Test
	void conflictingContentIs409() {
		List<ParameterContentHash.Row> rows = List.of(new ParameterContentHash.Row("case.entry.dpd", "PROD", "90"));
		when(validator.validate(any(), eq(TODAY), eq(TODAY))).thenReturn(rows);
		when(values.findByContent(any(), anyString())).thenReturn(List.of());
		when(values.save(any())).thenThrow(new DataIntegrityViolationException("synthetic unique violation"));

		assertThatThrownBy(() -> handler.load(csv("case.entry.dpd,PROD,90\n"), TODAY, AUTHOR))
			.isInstanceOf(ApiProblemException.class)
			.satisfies(ex -> assertThat(((ApiProblemException) ex).messageId()).isEqualTo("MSG-GEN-004"));
	}

	/** Ponytail Should 3: the unique index race becomes 409, never a 500. */
	@Test
	void anApprovalUniqueViolationIs409() {
		ParameterValueEntity pending = row(AUTHOR, "VALIDATED", TODAY);
		when(values.lockByLoadId(LOAD)).thenReturn(List.of(pending));
		when(values.findApproved(anyList())).thenReturn(List.of());
		org.mockito.Mockito.doThrow(approvalConflict()).when(values).flush();

		assertThatThrownBy(() -> handler.approve(LOAD, APPROVER))
			.isInstanceOf(ApiProblemException.class)
			.satisfies(ex -> {
				ApiProblemException problem = (ApiProblemException) ex;
				assertThat(problem.messageId()).isEqualTo("MSG-GEN-004");
				assertThat(problem.status().value()).isEqualTo(409);
			});
		verify(events, never()).publishEvent(any());
	}

	/** Ponytail New 10: a recorder that raises an integrity failure keeps the 503 MSG-P7-003 mapping. */
	@Test
	void aRecorderIntegrityFailureIs503() {
		ParameterValueEntity pending = row(AUTHOR, "VALIDATED", TODAY);
		when(values.lockByLoadId(LOAD)).thenReturn(List.of(pending));
		when(values.findApproved(anyList())).thenReturn(List.of());
		DataIntegrityViolationException recorderFailure = new DataIntegrityViolationException(
				"decision_log_entry unique violation");
		org.mockito.Mockito.doThrow(recorderFailure)
			.when(recorder)
			.recorded(eq("AC-VERS"), eq("APPROVED"), eq("PARAMETER"), eq(LOAD), anyList(), eq(TODAY), eq(APPROVER));

		assertThatThrownBy(() -> handler.approve(LOAD, APPROVER))
			.isInstanceOf(ApiProblemException.class)
			.satisfies(ex -> {
				ApiProblemException problem = (ApiProblemException) ex;
				assertThat(problem.messageId()).isEqualTo("MSG-P7-003");
				assertThat(problem.status().value()).isEqualTo(503);
				assertThat(problem.placeholders()).isEmpty();
			});
		verify(events, never()).publishEvent(any());
	}

	/** Ponytail New 10: an unrelated constraint keeps its own mapping and is never 409 MSG-GEN-004. */
	@Test
	void anUnrelatedIntegrityFailureIsNotAConflict() {
		ParameterValueEntity pending = row(AUTHOR, "VALIDATED", TODAY);
		when(values.lockByLoadId(LOAD)).thenReturn(List.of(pending));
		when(values.findApproved(anyList())).thenReturn(List.of());
		org.mockito.Mockito.doThrow(new DataIntegrityViolationException(
				"violates check constraint ck_parameter_value_approved_at",
				new java.sql.SQLException("check violation", "23514")))
			.when(values)
			.flush();

		assertThatThrownBy(() -> handler.approve(LOAD, APPROVER))
			.isInstanceOf(DataIntegrityViolationException.class);
	}

	/** The shape Hibernate raises for the approval index: unique violation plus the index name. */
	private static DataIntegrityViolationException approvalConflict() {
		return new DataIntegrityViolationException(
				"duplicate key value violates unique constraint \"ux_parameter_value_approved_from\"",
				new java.sql.SQLException("duplicate key", "23505"));
	}

	/** SEC-042-04: the approval event is published after the transaction commits, never inside it. */
	@Test
	void theApprovalEventIsPublishedAfterTheTransaction() {
		ParameterValueEntity pending = row(AUTHOR, "VALIDATED", TODAY);
		when(values.lockByLoadId(LOAD)).thenReturn(List.of(pending));
		when(values.findApproved(anyList())).thenReturn(List.of());
		RecordingTransactionManager transactions = new RecordingTransactionManager();
		ParameterLoadHandlerImpl recording = new ParameterLoadHandlerImpl(values, validator, recorder,
				() -> TODAY, events, mock(ParameterCache.class), transactions);
		java.util.concurrent.atomic.AtomicBoolean committedAtPublish = new java.util.concurrent.atomic.AtomicBoolean();
		org.mockito.Mockito.doAnswer(invocation -> {
			committedAtPublish.set(transactions.committed);
			return null;
		}).when(events).publishEvent(any(ParameterVersionApproved.class));

		recording.approve(LOAD, APPROVER);

		verify(events).publishEvent(any(ParameterVersionApproved.class));
		assertThat(committedAtPublish.get()).as("published before the commit").isTrue();
	}

	/** A stub manager that records the commit, so the test can order the event against it. */
	static final class RecordingTransactionManager extends StubTransactionManager {

		private boolean committed;

		@Override
		protected void doCommit(org.springframework.transaction.support.DefaultTransactionStatus status) {
			committed = true;
		}
	}

	@Test
	void findOfAnUnknownIdIsEmptyAndDoesNotThrow() {
		when(values.findByLoadId(LOAD)).thenReturn(List.of());

		assertThat(handler.find(LOAD)).isEmpty();
		assertThat(handler.find(null)).isEmpty();
	}

	@Test
	void unknownLoadIdIs404ForApproveAndRollback() {
		when(values.lockByLoadId(LOAD)).thenReturn(List.of());

		assertThatThrownBy(() -> handler.approve(LOAD, APPROVER))
			.isInstanceOf(ApiProblemException.class)
			.satisfies(ex -> assertThat(((ApiProblemException) ex).error().messageCode()).isEqualTo("MSG-P4-003"));
		assertThatThrownBy(() -> handler.rollback(LOAD, "synthetic reason", APPROVER))
			.isInstanceOf(ApiProblemException.class)
			.satisfies(ex -> assertThat(((ApiProblemException) ex).error().messageCode()).isEqualTo("MSG-P4-003"));
	}

	@Test
	void findOfALoadReturnsItsResult() {
		ParameterValueEntity stored = row(AUTHOR, "VALIDATED", TODAY);
		stored.loadId = LOAD;
		when(values.findByLoadId(LOAD)).thenReturn(List.of(stored));

		Optional<ParameterLoadResult> result = handler.find(LOAD);

		assertThat(result).isPresent();
		assertThat(result.orElseThrow().rows()).isEqualTo(1);
		assertThat(result.orElseThrow().table()).isEqualTo("PARAMETER");
	}

	private static java.io.InputStream csv(String text) {
		return new java.io.ByteArrayInputStream(text.getBytes(StandardCharsets.UTF_8));
	}

	private static ParameterValueEntity row(UUID author, String status, LocalDate validFrom) {
		ParameterValueEntity row = new ParameterValueEntity();
		row.id = UUID.randomUUID();
		row.paramKey = "case.entry.dpd";
		row.environment = "PROD";
		row.paramValue = "90";
		row.versionNo = 1;
		row.validFrom = validFrom;
		row.status = status;
		row.authorUserId = author;
		row.loadId = LOAD;
		row.version = 1;
		return row;
	}
}
