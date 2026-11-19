package th.co.scb.ace.demo.recovery.casewf.timers;

import java.time.Instant;
import java.util.UUID;

/**
 * Port for case timers (BS-5.2, ADR-011 T2). Epics 1 and 2 run it on Quartz; Epic 3 swaps in a
 * Temporal implementation without a caller change.
 */
public interface TimerScheduler {

	/** Schedules a timer. Scheduling the same timer ID again replaces the earlier due time. */
	void schedule(UUID timerId, UUID caseId, String timerCode, Instant dueAt);

	/** Cancels a timer. Returns false if no timer with that ID was scheduled. */
	boolean cancel(UUID timerId);

	/** Published when a timer falls due. Listeners must be idempotent on {@code timerId}. */
	record TimerDue(UUID timerId, UUID caseId, String timerCode, Instant dueAt) {
	}
}
